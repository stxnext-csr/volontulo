# -*- coding: utf-8 -*-

u"""
.. module:: views
"""

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import TemplateDoesNotExist

from . import models
from volontulo.forms import CreateOfferForm
from volontulo.forms import OfferApplyForm
from volontulo.forms import ProfileForm
from volontulo.forms import UserForm
from volontulo.models import UserProfile, Offer


def index(request):  # pylint: disable=unused-argument
    u"""Main view of app.

    I will just redirect of list of offers.
    """
    return redirect('list_offers')


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


def list_offers(request):
    u"""View, that show list of offers.

    It's used for volunteers to show active ones and for admins to show
    all of them.
    """
    if (
            request.user.is_authenticated() and
            models.UserProfile.objects.get(user=request.user).is_administrator
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


def create_offer(request):
    u"""View responsible for creating new offer by organization."""
    if request.method == 'POST':
        form = CreateOfferForm(request.POST)
        if form.is_valid():
            offer = form.save()
            domain = request.build_absolute_uri().replace(
                request.get_full_path(),
                ''
            )
            send_mail(
                u'Zgłoszenie oferty na Volontulo',
                u'ID oferty: {0}.'.format(offer.id),
                'support@volontuloapp.org',
                ['administrators@volontuloapp.org'],
                fail_silently=False,
                html_message=u'ID oferty: <a href="{0}{1}">{2}</a>.'.format(
                    domain,
                    reverse('show_offer', args=[offer.id]),
                    offer.id
                ),
            )
            messages.add_message(
                request,
                messages.INFO,
                u"Dziękujemy za dodanie oferty."
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                u"Formularz zawiera niepoprawnie wypełnione pola"
            )
            return render(
                request,
                'volontulo/create_offer.html',
                {
                    'form': form
                }
            )

    form = CreateOfferForm()
    return render(request, 'volontulo/create_offer.html', {'form': form})


def user_profile(request):
    u"""View to display user profile page."""
    user = get_object_or_404(UserProfile, user__email=request.user)

    return render(
        request,
        'volontulo/user_account.html',
        {
            'user': user
        }
    )


def organization_form(request):
    u"""View responsible for editing organization.

    Edition will only work, if logged user has been registered as organization.
    """
    if not (
            request.user.is_authenticated() and
            models.UserProfile.objects.get(user=request.user).is_organization
    ):
        return redirect('index')

    org = models.UserProfile.objects.get(user=request.user).organization
    if request.method == 'POST':
        org.name = request.POST.get('name')
        org.address = request.POST.get('address')
        org.description = request.POST.get('description')
        org.save()
        return HttpResponseRedirect(reverse('organization_form'))

    return render(
        request,
        "volontulo/organization_form.html",
        {'organization': org},
    )


def organization_view(request, organization_id):
    u"""View responsible for viewing organization."""
    org = get_object_or_404(models.Organization, id=organization_id)
    return render(
        request,
        "volontulo/organization_view.html",
        {'organization': org},
    )


def offer_apply(request, offer_id):
    u"""Handling volounteer applying for helping with offer."""
    if request.method == 'POST':
        form = OfferApplyForm(request.POST)
        if form.is_valid():
            domain = request.build_absolute_uri().replace(
                request.get_full_path(),
                ''
            )
            offer = Offer.objects.get(pk=offer_id)
            user = UserProfile.objects.get(
                organization__id=offer.organization.id
            )
            mail_content = u"""
                Email wolontariusza: {email}
                Numer telefonu: {phone_no}
                Imię i nazwisko: {fullname}
                Uwagi: {comments}
                ID oferty: {offer_id}
            """.format(
                email=request.POST.get('email'),
                phone_no=request.POST.get('phone_no'),
                fullname=request.POST.get('fullname'),
                comments=request.POST.get('comments'),
                offer_id=offer_id,
            )
            html_mail_content = u"""
                Email wolontariusza: {email}<br />
                Numer telefonu: {phone_no}<br />
                Imię i nazwisko: {fullname}<br />
                Uwagi: {comments}<br />
                ID oferty: <a href="{offer_url}">{offer_id}</a><br />
            """.format(
                email=request.POST.get('email'),
                phone_no=request.POST.get('phone_no'),
                fullname=request.POST.get('fullname'),
                comments=request.POST.get('comments'),
                offer_url=domain + reverse('show_offer', args=[offer_id]),
                offer_id=offer_id
            )
            send_mail(
                u'Zgłoszenie chęci pomocy w ofercie',
                mail_content,
                'support@volontuloapp.org',
                [
                    user.user.email,
                    request.POST.get('email'),
                ],
                fail_silently=False,
                html_message=html_mail_content,
            )
            messages.add_message(
                request,
                messages.SUCCESS,
                u'Zgłoszenie chęci uczestnictwa zostało wysłane'
            )
            return redirect(reverse('show_offer', args=[offer_id]))
        else:
            messages.add_message(
                request,
                messages.ERROR,
                u'Formularz zawiera nieprawidłowe dane' + form.errors
            )
            return render(
                request,
                'volontulo/offer_apply.html',
                {
                    'form': form,
                    'offer_id': offer_id,
                }
            )
    else:
        form = OfferApplyForm()
        return render(
            request,
            'volontulo/offer_apply.html',
            {
                'form': form,
                'offer_id': offer_id,
            }
        )
