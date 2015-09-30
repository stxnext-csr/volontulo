# -*- coding: utf-8 -*-

u"""
.. module:: __init__
"""

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import TemplateDoesNotExist

from volontulo.utils import yield_message_error
from volontulo.utils import yield_message_successful
from volontulo.forms import AdministratorContactForm
from volontulo.forms import ProfileForm
from volontulo.forms import UserForm
from volontulo.lib.email import send_mail
from volontulo.models import Offer
from volontulo.models import Organization
from volontulo.models import UserBadges
from volontulo.models import UserProfile


def logged_as_admin(request):
    u""""Helper function that provide information is user has admin privilege.

    It is used in separate modules.
    """
    return (
        request.user.is_authenticated() and
        UserProfile.objects.get(user=request.user).is_administrator
    )


def homepage(request):  # pylint: disable=unused-argument
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
        offers = Offer.objects.filter(status='ACTIVE')

    return render(
        request,
        "homepage.html",
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
        return redirect('homepage')
    else:
        return render(
            request,
            'users/login.html',
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
    return redirect('homepage')


def static_pages(request, template_name):
    u"""Generic view used for rendering static pages."""
    try:
        return render(
            request,
            "pages/{}.html".format(template_name)
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
                return redirect('register')
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
                profile.save()

                send_mail('registration', [user.email])
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    u'Rejestracja przebiegła pomyślnie'
                )
                return redirect('register')
        else:
            messages.add_message(
                request,
                messages.ERROR,
                u'Wprowadzono nieprawidłowy email lub hasło'
            )
            return redirect('register')

    user_form = UserForm()
    profile_form = ProfileForm()
    return render(
        request,
        'users/register.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )


def logged_user_profile(request):
    u"""View to display user profile page."""
    userprofile = UserProfile.objects.get(user=request.user)
    badges = UserBadges.objects\
        .filter(userprofile=userprofile.id)\
        .values('badge_id', 'badge__name', 'badge__priority')\
        .annotate(badges=Count('badge_id'))\
        .order_by('-badge__priority')
    ctx = {
        'badges': badges,
    }
    if not userprofile.organizations.count():
        ctx['offers'] = Offer.objects.filter(volunteers=request.user.id)

    return render(
        request,
        'users/user_profile.html',
        ctx
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
            yield_message_successful(request, u'Email został wysłany.')
        else:
            errors = u'<br />'.join(form.errors)
            yield_message_error(
                request,
                u'Proszę poprawić błędy w formularzu: ' + errors
            )
            return render(
                request,
                "contact.html",
                {
                    'contact_form': form,
                }
            )

    form = AdministratorContactForm()
    return render(
        request,
        "contact.html",
        {
            'contact_form': form,
        }
    )
