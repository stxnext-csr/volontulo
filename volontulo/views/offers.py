# -*- coding: utf-8 -*-

u"""
.. module:: offers
"""

from django.contrib import messages
from django.contrib.admin.models import ADDITION
from django.contrib.admin.models import CHANGE
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.text import slugify
from django.views.generic import View

from volontulo.forms import CreateOfferForm
from volontulo.forms import OfferApplyForm
from volontulo.lib.email import send_mail
from volontulo.models import Offer
from volontulo.models import UserProfile
from volontulo.utils import OFFERS_STATUSES
from volontulo.utils import save_history
from volontulo.utils import correct_slug
from volontulo.views import logged_as_admin


def offers_list(request):
    u"""View, that show list of offers.

    It's used for volunteers to show active ones and for admins to show
    all of them.
    """
    if logged_as_admin(request):
        offers = Offer.objects.all()
    else:
        offers = Offer.objects.filter(status='ACTIVE')
    return render(request, "offers/offers_list.html", context={
        'offers': offers,
    })


class OffersCreate(View):
    u"""Class view supporting creation of new offer."""

    @staticmethod
    def get(request):
        u"""Method responsible for rendering form for new offer."""
        user = UserProfile.objects.get(user=request.user)
        organization = user.organization

        form = CreateOfferForm()
        context = {
            'offer_form': form,
            'organization': organization,
            'statuses': OFFERS_STATUSES,
            'offer': Offer(),
        }

        return render(
            request,
            'offers/offer_form.html',
            context
        )

    @staticmethod
    def post(request):
        u"""Method resposible for saving new offer."""
        user = UserProfile.objects.get(user=request.user)
        organization = user.organization
        form = CreateOfferForm(request.POST)

        if form.is_valid():
            offer = form.save()
            save_history(request, offer, action=ADDITION)
            ctx = {
                'domain': request.build_absolute_uri().replace(
                    request.get_full_path(),
                    ''
                ),
                'address_sufix': reverse(
                    'offers_view',
                    args=[organization.id, offer.id]
                ),
                'offer': offer
            }
            send_mail(
                'offer_creation',
                ['administrators@volontuloapp.org'],
                ctx
            )
            messages.add_message(
                request,
                messages.SUCCESS,
                u"Dziękujemy za dodanie oferty."
            )
            return redirect(
                reverse(
                    'offers_view',
                    args=[organization.id, offer.id]
                ),
            )
        messages.add_message(
            request,
            messages.ERROR,
            u"Formularz zawiera niepoprawnie wypełnione pola"
        )
        return render(
            request,
            'offers/offer_form.html',
            {
                'offer_form': form,
                'organization': organization,
                'statuses': OFFERS_STATUSES,
                'user': user,
                'offer': Offer()
            }
        )


class OffersEdit(View):
    u"""Class view supporting change of a offer."""

    @staticmethod
    @correct_slug(Offer, 'offers_edit', 'title')
    def get(request, slug, id_):  # pylint: disable=unused-argument
        u"""Method responsible for rendering form for offer to be changed."""
        offer = Offer.objects.get(pk=id_)
        organization = offer.organization
        form = CreateOfferForm()

        context = {
            'offer_form': form,
            'organization': organization,
            'statuses': OFFERS_STATUSES,
            'offer': offer,
        }

        return render(
            request,
            'offers/offer_form.html',
            context
        )

    @staticmethod
    def post(request, slug, id_):  # pylint: disable=unused-argument
        u"""Method resposible for saving changed offer."""
        offer = Offer.objects.get(pk=id_)

        if request.POST['edit_type'] == 'status_change':
            offer.status = request.POST['status']
            offer.save()
            return redirect('offers_list')

        organization = offer.organization
        user = UserProfile.objects.get(user=request.user)
        form = CreateOfferForm(request.POST, instance=offer)

        if form.is_valid():
            offer = form.save()
            save_history(request, offer, action=CHANGE)
            messages.add_message(
                request,
                messages.SUCCESS,
                u"Oferta została zmieniona."
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                u"Formularz zawiera niepoprawnie wypełnione pola"
            )
        return render(
            request,
            'offers/offer_form.html',
            {
                'offer_form': form,
                'organization': organization,
                'statuses': OFFERS_STATUSES,
                'user': user,
                'offer': Offer()
            }
        )


@correct_slug(Offer, 'offers_view', 'title')
def offers_view(request, slug, id_):  # pylint: disable=unused-argument
    u"""View responsible for showing details of particular offer."""
    offer = get_object_or_404(Offer, id=id_)
    context = {
        'offer': offer,
    }
    user = UserProfile.objects.filter(user__id=request.user.id)[0]
    if user.is_administrator:
        context['user'] = user
        context['volunteers'] = offer.volunteers.all()
    return render(request, "offers/show_offer.html", context=context)


@correct_slug(Offer, 'offers_view', 'title')
def offers_join(request, slug, id_):  # pylint: disable=unused-argument
    u"""Handling volounteer applying for helping with offer."""
    offer = Offer.objects.get(pk=id_)

    if request.method == 'POST':
        form = OfferApplyForm(request.POST)
        if form.is_valid():
            domain = request.build_absolute_uri().replace(
                request.get_full_path(),
                ''
            )
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
                    offer_url=domain + reverse(
                        'offers_view',
                        args=[slugify(offer.title), id_]),
                    offer_id=id_
                )
            )
            messages.add_message(request,
                                 messages.SUCCESS,
                                 u'Zgłoszenie chęci uczestnictwa'
                                 u' zostało wysłane.')
            return redirect(
                reverse(
                    'offers_view',
                    args=[slugify(offer.title), id_]
                ),
            )
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
                    'offer_id': id_,
                }
            )
    else:
        form = OfferApplyForm()

    return render(
        request,
        'offers/offer_apply.html',
        {
            'form': form,
            'offer': offer,
        }
    )
