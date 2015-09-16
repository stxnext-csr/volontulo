# -*- coding: utf-8 -*-

u"""
.. module:: views
"""

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import TemplateDoesNotExist

from . import models
from volontulo.forms import UserForm
from volontulo.forms import ProfileForm


def index(request):  # pylint: disable=unused-argument
    u"""Main view of app.

    Right now there's not too much.
    """
    return HttpResponse(u"Welcome in volontulo app.")


def login(request):
    u"""Login view."""
    if request.method == 'GET':
        return render(request, "volontulo/login.html")
    username = request.POST['login']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponse(u"Poprawnie zalogowano")
        else:
            return HttpResponse(u"Konto zostało wyłączone!")
    else:
        return HttpResponse(u"Nieprawidłowy email lub hasło!")


def logout(request):
    u"""Logout view."""
    auth.logout(request)
    return HttpResponse(u"it's logout.")


def list_offers(request):
    u"""View, that show list of offers.

    It's used for volunteers to show active ones and for admins to show
    all of them.
    """
    if (
            request.user.is_authenticated() and
            models.UserProfile.objects.get(user=request.user).is_admin
    ):
        offers = models.Offer.objects.all()
    else:
        offers = models.Offer.objects.filter(status='ACTIVE')
    return render(request, "volontulo/list_offers.html", context={
        'offers': offers,
    })


def activate_offer(request, offer_id):  # pylint: disable=unused-argument
    u"""View responsible for changing status of offer from STAGED to ACTIVE."""
    offer = get_object_or_404(models.Offer, id=offer_id)
    offer.status = 'ACTIVE'
    offer.save()
    return redirect('list_offers')


def show_offer(request, offer_id):
    u"""View responsible for showing details of particular offer."""
    offer = get_object_or_404(models.Offer, id=offer_id)
    return render(request, "volontulo/show_offer.html", context={
        'offer': offer,
    })


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
                    org = models.Organization(name=profile.user)
                    org.save()
                    profile.organization = org

                profile.save()

                send_mail(
                    u'Rejestracja na Volontulo',
                    u'Dziękujemy za rejestrację.',
                    'support@volontulo.org',
                    [user.email],
                    fail_silently=False
                )
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
