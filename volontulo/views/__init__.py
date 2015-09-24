# -*- coding: utf-8 -*-

u"""
.. module:: __init__
"""

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import TemplateDoesNotExist

from volontulo.forms import AdministratorContactForm
from volontulo.forms import ProfileForm
from volontulo.forms import UserForm
from volontulo.lib.email import send_mail
from volontulo.models import Offer
from volontulo.models import Organization
from volontulo.models import UserProfile


def logged_as_admin(request):
    u""""Helper function that provide information is user has admin privilege.

    It is used in separate modules.
    """
    return (
        request.user.is_authenticated() and
        UserProfile.objects.get(user=request.user).is_administrator
    )


# todo: replace with more generic
def yield_message_successful_email(request):
    u"""Helper function yielding info about successful email."""
    return messages.add_message(
        request,
        messages.SUCCESS,
        u'Email został wysłany.'
    )


# todo: replace with more generic
def yield_message_error_form(request, form):
    u"""Helper function yielding info about errors in form."""
    return messages.add_message(
        request,
        messages.ERROR,
        u'Proszę poprawić błędy w formularzu: ' + u'<br />'.join(form.errors)
    )


def yield_message_successful(request, msg):
    u"""Helper function yielding success message."""
    return messages.add_message(request, messages.SUCCESS, msg)


def yield_message_error(request, msg):
    u"""Helper function yielding error message."""
    return messages.add_message(request, messages.ERROR, msg)


def index(request):  # pylint: disable=unused-argument
    u"""Main view of app.

    We will display page with few step CTA links?
    """
    if logged_as_admin(request):
        # implement ON/OFF statuses
        offers = Offer.objects.all().order_by('-status')
        return render(request, "admin/list_offers.html", context={
            'offers': offers,
        })
    else:
        offers = Offer.objects.filter(status='STAGED')

    return render(
        request,
        "volontulo/homepage.html",
        {
            'offers': offers,
        }
    )


def login(request):
    u"""Login view."""
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    u"Poprawnie zalogowano"
                )

            else:
                messages.add_message(
                    request,
                    messages.INFO,
                    u"Konto zostało wyłączone!"
                )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                u"Nieprawidłowy email lub hasło!"
            )
        return redirect('index')
    else:
        return render(
            request,
            'volontulo/login.html',
            {}
        )


@login_required
def logout(request):
    u"""Logout view."""
    auth.logout(request)
    messages.add_message(
        request,
        messages.INFO,
        u"Użytkownik został wylogowany!"
    )
    return redirect('index')


def static_pages(request, template_name):
    u"""Generic view used for rendering static pages."""
    try:
        return render(
            request,
            "volontulo/static_pages/{}.html".format(template_name)
        )
    except TemplateDoesNotExist:
        raise Http404


def register(request):
    u"""View responsible for registering new users."""
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                user = User.objects.get(email=request.POST.get('email'))
            except User.DoesNotExist:
                user = None
            if user:
                messages.add_message(
                    request,
                    messages.INFO,
                    u'Użytkownik o podanym emailu już istnieje'
                )
                return HttpResponseRedirect(reverse('register'))
            else:
                # save user
                user = user_form.save(commit=False)
                user.set_password(request.POST.get('password'))
                # to prevent username UNIQUE constraint
                user.username = user.email
                user.save()
                # save profile
                profile = profile_form.save(commit=False)
                profile.user = user

                # 87 - if user check, that he/she's representing organization
                # we need to create new organization and link it to this user:
                if profile.is_organization:
                    org = Organization(name=profile.user)
                    org.save()
                    profile.organization = org

                profile.save()

                send_mail('registration', [user.email])
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    u'Rejestracja przebiegła pomyślnie'
                )
                return HttpResponseRedirect(reverse('register'))
        else:
            messages.add_message(
                request,
                messages.ERROR,
                u'Wprowadzono nieprawidłowy email lub hasło'
            )
            return HttpResponseRedirect(reverse('register'))

    user_form = UserForm()
    profile_form = ProfileForm()
    return render(
        request,
        'volontulo/register.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )


def logged_user_profile(request):
    u"""View to display user profile page."""
    user = get_object_or_404(UserProfile, user__email=request.user)
    offers = Offer.objects.filter(volunteers=user.id)

    return render(
        request,
        'users/user_profile.html',
        {
            'user': user,
            'offers': offers,
        }
    )


def contact_form(request):
    u"""View responsible for contact forms."""
    if request.method == 'POST':
        form = AdministratorContactForm(request.POST)
        if form.is_valid():
            # get administrators by IDS
            administrator_id = request.POST.get('administrator')
            admin = User.objects.get(pk=administrator_id)
            send_mail(
                'volunteer_to_admin',
                [
                    admin.email,
                    request.POST.get('email'),
                ],
                {k: v for k, v in request.POST.items()},
            )
            yield_message_successful_email(request)
        else:
            yield_message_error_form(request, form)
            return render(
                request,
                "volontulo/contact.html",
                {
                    'contact_form': form,
                }
            )

    form = AdministratorContactForm()
    return render(
        request,
        "volontulo/contact.html",
        {
            'contact_form': form,
        }
    )
