# -*- coding: utf-8 -*-

u"""
.. module:: views
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
from volontulo.forms import CreateOfferForm
from volontulo.forms import OfferApplyForm
from volontulo.forms import ProfileForm
from volontulo.forms import UserForm
from volontulo.forms import VolounteerToOrganizationContactForm
from volontulo.lib.email import send_mail
from volontulo.models import Offer
from volontulo.models import Organization
from volontulo.models import UserProfile


def index(request):  # pylint: disable=unused-argument
    u"""Main view of app.

    We will display page with few step CTA links?
    """
    if (
            request.user.is_authenticated() and
            UserProfile.objects.get(user=request.user).is_administrator
    ):
        offers = Offer.objects.all()
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


def list_offers(request):
    u"""View, that show list of offers.

    It's used for volunteers to show active ones and for admins to show
    all of them.
    """
    if (
            request.user.is_authenticated() and
            UserProfile.objects.get(user=request.user).is_administrator
    ):
        offers = Offer.objects.all()
    else:
        offers = Offer.objects.filter(status='ACTIVE')
    return render(request, "volontulo/list_offers.html", context={
        'offers': offers,
    })


def activate_offer(request, offer_id):  # pylint: disable=unused-argument
    u"""View responsible for changing status of offer from STAGED to ACTIVE."""
    offer = get_object_or_404(Offer, id=offer_id)
    offer.status = 'ACTIVE'
    offer.save()
    return redirect('list_offers')


def show_offer(request, offer_id):
    u"""View responsible for showing details of particular offer."""
    offer = get_object_or_404(Offer, id=offer_id)
    context = {
        'offer': offer,
    }
    user = UserProfile.objects.filter(user__id=request.user.id)[0]
    if user.is_administrator:
        context['user'] = user
        context['volunteers'] = offer.volunteers.all()
    return render(request, "volontulo/show_offer.html", context=context)


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


def offer_form(request, organization_id):
    u"""View responsible for creating and editing offer by organization."""
    organization = Organization.objects.get(pk=organization_id)
    if request.method == 'POST':
        form = CreateOfferForm(request.POST)
        if form.is_valid():
            offer = form.save()
            domain = request.build_absolute_uri().replace(
                request.get_full_path(),
                ''
            )
            send_mail('offer_creation', ['administrators@volontuloapp.org'], {
                'domain': domain,
                'address_sufix': reverse('show_offer', args=[offer.id]),
                'offer': offer
            })
            messages.add_message(
                request,
                messages.SUCCESS,
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
                'volontulo/offer_form.html',
                {
                    'offer_form': form,
                    'organization': organization,
                }
            )
    form = CreateOfferForm()
    return render(request, 'volontulo/offer_form.html', {
        'offer_form': form,
        'organization': organization,
    })


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


def organization_form(request):
    u"""View responsible for editing organization.

    Edition will only work, if logged user has been registered as organization.
    """
    if not (
            request.user.is_authenticated() and
            UserProfile.objects.get(user=request.user).is_organization
    ):
        return redirect('index')

    org = UserProfile.objects.get(user=request.user).organization
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


# pylint: disable=unused-argument
def organization_view(request, slug, organization_id):
    u"""View responsible for viewing organization."""
    org = get_object_or_404(Organization, id=organization_id)
    offers = Offer.objects.filter(organization_id=organization_id)
    if request.method == 'POST':
        form = VolounteerToOrganizationContactForm(request.POST)
        if form.is_valid():
            profile = UserProfile.objects.get(organization_id=organization_id)
            send_mail(
                'volunteer_to_organisation',
                [
                    profile.user.email,
                    request.POST.get('email'),
                ],
                dict(
                    name=request.POST.get('name'),
                    email=request.POST.get('email'),
                    phone_no=request.POST.get('phone_no'),
                    message=request.POST.get('message'),
                )
            )
            messages.add_message(
                request,
                messages.SUCCESS,
                u"Email został wysłany"
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                u"Proszę poprawić błędy w formularzu: " +
                "<br />".join(form.errors)
            )
            return render(
                request,
                "volontulo/organization_view.html",
                {
                    'organization': org,
                    'contact_form': form,
                    'offers': offers,
                },
            )
    form = VolounteerToOrganizationContactForm()
    return render(
        request,
        "volontulo/organization_view.html",
        {
            'organization': org,
            'contact_form': form,
            'offers': offers,
        },
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
                dict(
                    name=request.POST.get('name'),
                    email=request.POST.get('email'),
                    phone_no=request.POST.get('phone_no'),
                    applicant=request.POST.get('applicant'),
                    message=request.POST.get('message'),
                )
            )
            messages.add_message(
                request,
                messages.SUCCESS,
                u'Wiadomość została wysłana do administratora'
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                u'Proszę poprawić błędy w formularzu: ' +
                '<br />'.join(form.errors)
            )
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
            if request.user.id:
                volunteer = User.objects.get(pk=request.user.id)
                offer.volunteers.add(volunteer)
                offer.save()

            send_mail(
                'offer_application',
                [
                    user.user.email,
                    request.POST.get('email'),
                ],
                dict(
                    email=request.POST.get('email'),
                    phone_no=request.POST.get('phone_no'),
                    fullname=request.POST.get('fullname'),
                    comments=request.POST.get('comments'),
                    offer_url=domain + reverse('show_offer', args=[offer_id]),
                    offer_id=offer_id
                )
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
