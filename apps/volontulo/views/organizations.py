# -*- coding: utf-8 -*-

u"""
.. module:: organizations
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.text import slugify
from django.views.generic import View

from apps.volontulo.forms import VolounteerToOrganizationContactForm
from apps.volontulo.lib.email import send_mail
from apps.volontulo.models import Offer
from apps.volontulo.models import Organization
from apps.volontulo.models import UserProfile
from apps.volontulo.utils import correct_slug


def organizations_list(request):
    u"""View responsible for listing all organizations.

    :param request: WSGIRequest instance
    """
    organizations = Organization.objects.all()
    return render(
        request,
        "organizations/list.html",
        {'organizations': organizations},
    )


class OrganizationsCreate(View):
    u"""Class view supporting creation of new organization."""

    @staticmethod
    @login_required
    def get(request):
        u"""Method responsible for rendering form for new organization."""
        return render(
            request,
            "organizations/organization_form.html",
            {'organization': Organization()}
        )

    @staticmethod
    @login_required
    def post(request):
        u"""Method responsible for saving new organization."""
        if not (
                request.POST.get('name') and
                request.POST.get('address') and
                request.POST.get('description')
        ):
            messages.error(
                request,
                u"Należy wypełnić wszystkie pola formularza."
            )
            return render(
                request,
                "organizations/organization_form.html",
                {'organization': Organization()}
            )

        organization = Organization(
            name=request.POST.get('name'),
            address=request.POST.get('address'),
            description=request.POST.get('description'),
        )
        organization.save()
        request.user.userprofile.organizations.add(organization)
        messages.success(
            request,
            u"Organizacja została dodana."
        )
        return redirect(
            'organization_view',
            slug=slugify(organization.name),
            id_=organization.id,
        )


@correct_slug(Organization, 'organization_form', 'name')
@login_required
def organization_form(request, slug, id_):  # pylint: disable=unused-argument
    u"""View responsible for editing organization.

    Edition will only work, if logged user has been registered as organization.
    """
    org = Organization.objects.get(pk=id_)
    users = [profile.user.email for profile in org.userprofiles.all()]
    if (
            request.user.is_authenticated() and
            request.user.email not in users
    ):
        messages.error(
            request,
            u'Nie masz uprawnień do edycji tej organizacji.'
        )
        return redirect(
            reverse(
                'organization_view',
                args=[slugify(org.name), org.id]
            )
        )

    if not (
            request.user.is_authenticated() and
            UserProfile.objects.get(user=request.user).organizations
    ):
        return redirect('homepage')

    if request.method == 'POST':
        if (
                request.POST.get('name') and
                request.POST.get('address') and
                request.POST.get('description')
        ):
            org.name = request.POST.get('name')
            org.address = request.POST.get('address')
            org.description = request.POST.get('description')
            org.save()
            messages.success(
                request,
                u'Oferta została dodana/zmieniona.'
            )
            return redirect(
                reverse(
                    'organization_view',
                    args=[slugify(org.name), org.id]
                )
            )
        else:
            messages.error(
                request,
                u"Należy wypełnić wszystkie pola formularza."
            )

    return render(
        request,
        "organizations/organization_form.html",
        {'organization': org},
    )


@correct_slug(Organization, 'organization_view', 'name')
def organization_view(request, slug, id_):  # pylint: disable=unused-argument
    u"""View responsible for viewing organization."""
    org = get_object_or_404(Organization, id=id_)
    offers = Offer.objects.filter(organization_id=id_)
    allow_contact = True
    allow_edit = False
    allow_offer_create = False
    if (
            request.user.is_authenticated() and
            request.user.userprofile in org.userprofiles.all()
    ):
        allow_contact = False
        allow_edit = True
        allow_offer_create = True

    if request.method == 'POST':
        form = VolounteerToOrganizationContactForm(request.POST)
        if form.is_valid():
            # send email to first organization user (I assume it's main user)
            profile = Organization.objects.get(id=id_).userprofiles.all()[0]
            send_mail(
                request,
                'volunteer_to_organisation',
                [
                    profile.user.email,
                    request.POST.get('email'),
                ],
                {k: v for k, v in request.POST.items()},
            )
            messages.success(request, u'Email został wysłany.')
        else:
            messages.error(
                request,
                u"Formularz zawiera nieprawidłowe dane: {}".format(form.errors)
            )
            return render(
                request,
                "organizations/organization_view.html",
                {
                    'organization': org,
                    'contact_form': form,
                    'offers': offers,
                    'allow_contact': allow_contact,
                    'allow_edit': allow_edit,
                    'allow_offer_create': allow_offer_create,
                },
            )
    return render(
        request,
        "organizations/organization_view.html",
        {
            'organization': org,
            'contact_form': VolounteerToOrganizationContactForm(),
            'offers': offers,
            'allow_contact': allow_contact,
            'allow_edit': allow_edit,
            'allow_offer_create': allow_offer_create,
        }
    )
