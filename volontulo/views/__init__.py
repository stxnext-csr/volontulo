# -*- coding: utf-8 -*-

u"""
.. module:: __init__
"""
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from django.template import TemplateDoesNotExist

from volontulo.forms import AdministratorContactForm
from volontulo.forms import UserGalleryForm
from volontulo.lib.email import send_mail
from volontulo.models import Offer
from volontulo.models import UserBadges
from volontulo.models import UserProfile
from volontulo.utils import yield_message_error
from volontulo.utils import yield_message_successful


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


def static_pages(request, template_name):
    u"""Generic view used for rendering static pages."""
    try:
        return render(
            request,
            "pages/{}.html".format(template_name)
        )
    except TemplateDoesNotExist:
        raise Http404


@login_required
def logged_user_profile(request):
    u"""View to display user profile page."""
    userprofile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST' and request.FILES:
        handle_file_upload(request, userprofile)

    ctx = {
        'badges': UserBadges.get_user_badges(userprofile),
        'image': UserGalleryForm(),
        'userprofile': userprofile,
        'MEDIA_URL': settings.MEDIA_URL
    }

    # Current user is organization
    if userprofile.organizations.count():
        ctx['offers'] = Offer.objects.filter(
            organization__userprofiles__user=request.user
        )
    else:
        # get offers that volunteer applied
        ctx['offers'] = Offer.objects.filter(volunteers=request.user)

    return render(request, 'users/user_profile.html', ctx)


def handle_file_upload(request, userprofile):
    u"""Handle image upload for user profile page."""
    gallery_form = UserGalleryForm(request.POST, request.FILES)
    if gallery_form.is_valid():
        # validate file extension (content type)
        gallery = gallery_form.save(commit=False)
        gallery.userprofile = userprofile
        gallery.is_avatar = True if request.POST.get('is_avatar') else False
        gallery.save()
        yield_message_successful(request, u"Dodano grafikę")
    else:
        errors = '<br />'.join(gallery_form.errors)
        yield_message_error(
            request,
            u"Problem w trakcie dodawania grafiki: {}".format(errors)
        )


@login_required
def contact_form(request):
    u"""View responsible for contact forms."""
    if request.method == 'POST':
        form = AdministratorContactForm(request.POST)
        if form.is_valid():
            # get administrators by IDS
            administrator_id = request.POST.get('administrator')
            admin = User.objects.get(id=administrator_id)
            send_mail(
                request,
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
