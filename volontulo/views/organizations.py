# -*- coding: utf-8 -*-

u"""
.. module:: organizations
"""

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from volontulo.forms import VolounteerToOrganizationContactForm
from volontulo.lib.email import send_mail
from volontulo.models import Offer
from volontulo.models import Organization
from volontulo.models import UserProfile


# pylint: disable=unused-argument
def organization_form(request, slug, organization_id):
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
                {k: v for k, v in request.POST.items()},
            )
            messages.add_message(request,
                                 messages.SUCCESS,
                                 u'Email został wysłany')
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
