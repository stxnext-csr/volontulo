# -*- coding: utf-8 -*-

u"""
.. module:: offers
"""

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.models import ADDITION
from django.contrib.admin.models import CHANGE
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.text import slugify
from django.views.generic import View

from volontulo.forms import CreateOfferForm
from volontulo.forms import OfferApplyForm
from volontulo.forms import OfferImageForm
from volontulo.lib.email import send_mail
from volontulo.models import Offer
from volontulo.models import OfferImage
from volontulo.models import UserBadges
from volontulo.models import UserProfile
from volontulo.utils import correct_slug
from volontulo.utils import OFFERS_STATUSES
from volontulo.utils import save_history
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
        form = CreateOfferForm()
        context = {
            'offer_form': form,
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
        form = CreateOfferForm(request.POST)
        images = []

        if form.is_valid():
            offer = form.save()
            save_history(request, offer, action=ADDITION)
            ctx = {'offer': offer}
            send_mail(
                request,
                'offer_creation',
                ['administrators@volontuloapp.org'],
                ctx
            )
            messages.success(
                request,
                u"Dziękujemy za dodanie oferty."
            )
            return redirect(
                'offers_view',
                slug=slugify(offer.title),
                id_=offer.id,
            )
        messages.error(
            request,
            u"Formularz zawiera niepoprawnie wypełnione pola"
        )
        return render(
            request,
            'offers/offer_form.html',
            {
                'offer_form': form,
                'statuses': OFFERS_STATUSES,
                'offer': Offer(),
                'images': images,
            }
        )


class OffersEdit(View):
    u"""Class view supporting change of a offer."""

    @staticmethod
    @correct_slug(Offer, 'offers_edit', 'title')
    def get(request, slug, id_):  # pylint: disable=unused-argument
        u"""Method responsible for rendering form for offer to be changed."""
        offer = Offer.objects.get(id=id_)
        organization = offer.organization
        form = CreateOfferForm()
        offer_image_form = OfferImageForm()
        images = OfferImage.objects.filter(offer=offer).all()

        context = {
            'offer_form': form,
            'organization': organization,
            'statuses': OFFERS_STATUSES,
            'offer': offer,
            'offer_image_form': offer_image_form,
            'images': images,
            'MEDIA_URL': settings.MEDIA_URL
        }

        return render(
            request,
            'offers/offer_form.html',
            context
        )

    @staticmethod
    def post(request, slug, id_):  # pylint: disable=unused-argument
        u"""Method resposible for saving changed offer."""
        def _set_main_image(offer, gallery_form):
            u"""Set main image flag unsetting other offers images."""
            if gallery_form.cleaned_data["is_main"]:
                OfferImage.objects.filter(offer=offer).update(is_main=False)
                return True
            return False

        def _save_offer_image(offer, userprofile):
            u"""Handle image upload for user profile page."""
            gallery_form = OfferImageForm(
                request.POST,
                request.FILES
            )
            if gallery_form.is_valid():
                gallery = gallery_form.save(commit=False)
                gallery.offer = offer
                gallery.userprofile = userprofile
                gallery.is_main = _set_main_image(offer, gallery_form)
                gallery.save()
                messages.success(request, u"Dodano zdjęcie do galerii.")
            else:
                errors = '<br />'.join(gallery_form.errors)
                messages.error(
                    request,
                    u"Problem w trakcie dodawania grafiki: {}".format(errors)
                )
            return redirect(
                reverse(
                    'offers_edit',
                    args=[slugify(offer.title), offer.id]
                )
            )

        def _close_offer(offer):
            u"""Change offer status to close."""
            offer.status = 'CLOSED'
            offer.save()
            return redirect(
                reverse(
                    'offers_view',
                    args=[slugify(offer.title), offer.id]
                )
            )

        def _change_status(offer):
            u"""Change offer status."""
            offer.status = request.POST['status']
            offer.save()
            return redirect('offers_list')

        offer = Offer.objects.get(id=id_)
        if request.POST.get('submit') == 'save_image' and request.FILES:
            return _save_offer_image(offer, request.user.userprofile)
        elif request.POST.get('close_offer') == 'close':
            return _close_offer(offer)
        elif request.POST.get('edit_type') == 'status_change':
            return _change_status(offer)

        form = CreateOfferForm(request.POST, instance=offer)
        if form.is_valid():
            offer = form.save()
            save_history(request, offer, action=CHANGE)
            messages.success(
                request,
                u"Oferta została zmieniona."
            )
        else:
            messages.error(
                request,
                u"Formularz zawiera niepoprawnie wypełnione pola"
            )
        return render(
            request,
            'offers/offer_form.html',
            {
                'offer_form': form,
                'statuses': OFFERS_STATUSES,
                'offer': Offer()
            }
        )


class OffersView(View):
    u"""Class view supporting offer preview."""

    @staticmethod
    @correct_slug(Offer, 'offers_view', 'title')
    def get(request, slug, id_):  # pylint: disable=unused-argument
        u"""View responsible for showing details of particular offer."""
        offer = get_object_or_404(Offer, id=id_)
        try:
            main_image = OfferImage.objects.get(offer=offer, is_main=True)
        except OfferImage.DoesNotExist:
            main_image = ''

        context = {
            'offer': offer,
            'volunteers': offer.volunteers.all(),
            'MEDIA_URL': settings.MEDIA_URL,
            'main_image': main_image,
        }
        return render(request, "offers/show_offer.html", context=context)

    @staticmethod
    def post(request, slug, id_):  # pylint: disable=unused-argument
        u"""View responsible for submitting volunteers awarding."""
        offer = get_object_or_404(Offer, id=id_)
        post_data = request.POST
        if post_data.get('csrfmiddlewaretoken'):
            del post_data['csrfmiddlewaretoken']
        if post_data.get('submit'):
            del post_data['submit']

        offer_content_type = ContentType.objects.get(
            app_label='volontulo',
            model='offer'
        )
        for award in post_data:
            userprofile_id = award.split('_')[1]
            volunteer_user = UserProfile.objects.get(id=userprofile_id)
            award_value = request.POST.get('award_%s' % userprofile_id)
            if award_value == 'PROMINENT-PARTICIPANT':
                UserBadges.apply_prominent_participant_badge(
                    offer_content_type,
                    volunteer_user,
                )
            elif award_value == 'NOT-APPLY':
                UserBadges.decrease_user_participant_badge(
                    offer_content_type,
                    volunteer_user,
                )
        offer.votes = True
        offer.save()

        context = {
            'offer': offer,
        }
        return render(request, "offers/show_offer.html", context=context)


class OffersJoin(View):
    u"""Class view supporting joining offer."""

    @staticmethod
    @correct_slug(Offer, 'offers_join', 'title')
    def get(request, slug, id_):  # pylint: disable=unused-argument
        u"""View responsible for showing join form for particular offer."""
        if request.user.is_authenticated():
            has_applied = Offer.objects.filter(
                volunteers=request.user,
                volunteers__offer=id_,
            ).count()
            if has_applied:
                messages.error(
                    request,
                    u'Już wyraziłeś chęć uczestnictwa w tej ofercie.'
                )
                return redirect('offers_list')

        offer = Offer.objects.get(id=id_)
        form = OfferApplyForm()
        context = {
            'form': form,
            'offer': offer,
        }

        context['volunteer_user'] = UserProfile()
        if request.user.is_authenticated():
            context['volunteer_user'] = request.user.userprofile

        return render(
            request,
            'offers/offer_apply.html',
            context
        )

    @staticmethod
    def post(request, slug, id_):  # pylint: disable=unused-argument
        u"""View responsible for saving join for particular offer."""
        form = OfferApplyForm(request.POST)

        if form.is_valid():
            offer = Offer.objects.get(id=id_)

            if request.user.is_authenticated():
                user = request.user
            else:
                try:
                    user = User.objects.create_user(
                        username=request.POST.get('email'),
                        email=request.POST.get('email'),
                        password=User.objects.make_random_password(),
                    )
                    profile = UserProfile(user=user)
                    profile.save()
                except IntegrityError:
                    messages.info(
                        request,
                        u'Użytkownik o podanym emailu już istnieje.'
                        u' Zaloguj się.'
                    )
                    return render(
                        request,
                        'offers/offer_apply.html',
                        {
                            'form': form,
                            'offer_id': id_,
                            'volunteer_user': UserProfile(),
                        }
                    )

            has_applied = Offer.objects.filter(
                volunteers=user,
                volunteers__offer=id_,
            ).count()
            if has_applied:
                messages.error(
                    request,
                    u'Już wyraziłeś chęć uczestnictwa w tej ofercie.'
                )
                return redirect('offers_list')

            offer_content_type = ContentType.objects.get(
                app_label='volontulo',
                model='offer'
            )

            offer.volunteers.add(user)
            UserBadges.apply_participant_badge(
                offer_content_type,
                user.userprofile,
            )
            offer.save()

            send_mail(
                request,
                'offer_application',
                [
                    user.email,
                    request.POST.get('email'),
                ],
                dict(
                    email=request.POST.get('email'),
                    phone_no=request.POST.get('phone_no'),
                    fullname=request.POST.get('fullname'),
                    comments=request.POST.get('comments'),
                    offer=offer,
                )
            )
            messages.success(
                request,
                u'Zgłoszenie chęci uczestnictwa zostało wysłane.'
            )
            return redirect(
                'offers_view',
                slug=slugify(offer.title),
                id_=offer.id,
            )
        else:
            errors = '<br />'.join(form.errors)
            messages.error(
                request,
                u'Formularz zawiera nieprawidłowe dane' + errors
            )
            volunteer_user = UserProfile()
            if request.user.is_authenticated():
                volunteer_user = request.user.userprofile
            return render(
                request,
                'offers/offer_apply.html',
                {
                    'form': form,
                    'offer_id': id_,
                    'volunteer_user': volunteer_user,
                }
            )
