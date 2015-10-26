# -*- coding: utf-8 -*-

u"""
.. module:: __init__
"""
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import TemplateDoesNotExist

from volontulo.utils import yield_message_error
from volontulo.utils import yield_message_successful
from volontulo.forms import AdministratorContactForm
from volontulo.forms import EditProfileForm
from volontulo.forms import OrganizationGalleryForm
from volontulo.forms import UserGalleryForm
from volontulo.lib.email import send_mail
from volontulo.models import Offer
from volontulo.models import OrganizationGallery
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
    def _init_edit_profile_form():
        u"""Initialize EditProfileForm - helper method."""
        return EditProfileForm(
            initial={
                'email': request.user.email,
                'user': request.user.id,
            }
        )

    def _populate_offers():
        u"""..."""
        if userprofile.organizations.count():
            # Current user is organization
            return Offer.objects.filter(
                organization__userprofiles__user=request.user
            )
        else:
            # get offers that volunteer applied
            return Offer.objects.filter(volunteers=request.user)

    def _is_saving_user_avatar():
        u"""."""
        return request.POST.get('submit') == 'save_image' and request.FILES

    def _is_saving_organization_image():
        u"""."""
        submit_value = request.POST.get('submit')
        return submit_value == 'save_organization_image' and request.FILES

    def _is_saving_profile():
        u"""."""
        return request.POST.get('submit') == 'save_profile'

    def _save_userprofile():
        u"""."""
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.set_password(profile_form.cleaned_data['new_password'])
            user.save()
            yield_message_successful(
                request,
                u"Zaktualizowano profil"
            )
        else:
            errors = '<br />'.join(profile_form.errors)
            yield_message_error(
                request,
                u"Problem w trakcie zapisywania profilu: {}".format(errors)
            )
        return form

    def _handle_user_avatar_upload():
        u"""Handle image upload for user profile page."""
        gallery_form = UserGalleryForm(request.POST, request.FILES)
        if gallery_form.is_valid():
            userprofile.clean_images()
            gallery = gallery_form.save(commit=False)
            gallery.userprofile = userprofile
            # User can only change his avatar
            gallery.is_avatar = True
            gallery.save()
            yield_message_successful(request, u"Dodano grafikę")
        else:
            errors = '<br />'.join(gallery_form.errors)
            yield_message_error(
                request,
                u"Problem w trakcie dodawania grafiki: {}".format(errors)
            )

    # pylint: disable=invalid-name
    def _handle_organization_image_upload():
        u"""Handle image upload for user profile page."""

        def _is_main(form):
            u"""Return True if is_main image was selected."""
            return True if form.cleaned_data['is_main'] else False

        gallery_form = OrganizationGalleryForm(
            userprofile,
            request.POST,
            request.FILES
        )
        if gallery_form.is_valid():
            gallery = gallery_form.save(commit=False)
            gallery.published_by = userprofile
            if _is_main(gallery_form):
                gallery.set_as_main(gallery.organization)
            gallery.save()
            yield_message_successful(request, u"Dodano zdjęcie do galerii.")
        else:
            errors = '<br />'.join(gallery_form.errors)
            yield_message_error(
                request,
                u"Problem w trakcie dodawania grafiki: {}".format(errors)
            )

    profile_form = _init_edit_profile_form()
    userprofile = UserProfile.objects.get(user=request.user)
    galleries = OrganizationGallery.get_organizations_galleries(
        userprofile
    )

    if request.method == 'POST':
        if _is_saving_user_avatar():
            _handle_user_avatar_upload()
        elif _is_saving_organization_image():
            _handle_organization_image_upload()
            return redirect('logged_user_profile')
        elif _is_saving_profile():
            profile_form = _save_userprofile()

    ctx = dict(
        badges=UserBadges.get_user_badges(userprofile),
        profile_form=profile_form,
        user_avatar_form=UserGalleryForm(),
        organization_image_form=OrganizationGalleryForm(userprofile),
        galleries=galleries,
        userprofile=userprofile,
        MEDIA_URL=settings.MEDIA_URL
    )
    ctx['offers'] = _populate_offers()
    return render(request, 'users/user_profile.html', ctx)


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


def page_not_found(request):
    u"""Page not found - 404 error handler."""
    return render(
        request,
        '404.html',
        status=404
    )


def server_error(request):
    u"""Internal Server Error - 500 error handler."""
    return render(
        request,
        '500.html',
    )
