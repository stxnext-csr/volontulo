# -*- coding: utf-8 -*-

u"""
.. module:: forms
"""
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.volontulo.models import Offer
from apps.volontulo.models import OfferImage
from apps.volontulo.models import Organization
from apps.volontulo.models import OrganizationGallery
from apps.volontulo.models import UserGallery
from apps.volontulo.utils import get_administrators_emails


class UserForm(forms.ModelForm):
    u"""Form reposponsible for authorization."""
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta(object):
        model = User
        fields = ['email']


class EditProfileForm(forms.Form):
    u"""Form reposponsible for edit user details on profile page."""
    email = forms.EmailField(label="Email")
    phone_no = forms.CharField(label=u"Phone number", required=False)
    current_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False
    )
    user = forms.CharField(widget=forms.HiddenInput())

    def is_valid(self):
        valid = super(EditProfileForm, self).is_valid()
        if not valid:
            return valid

        current_password = self.cleaned_data['current_password']
        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']
        user = User.objects.get(id=self.cleaned_data['user'])

        if (
                current_password and
                new_password and
                confirm_new_password
        ):
            if not user.check_password(current_password):
                raise ValidationError(u"Aktualne hasło jest błędne")

            if new_password != confirm_new_password:
                raise ValidationError(u"Wprowadzone hasła różnią się")

        return True


class CreateOfferForm(forms.ModelForm):
    u"""Form reposponsible for creating offer by organization."""

    def __init__(self, *args, **kwargs):
        super(CreateOfferForm, self).__init__(*args, **kwargs)
        self.fields['status_old'].required = False

    class Meta(object):
        model = Offer
        fields = [
            'organization',
            'description',
            'requirements',
            'time_commitment',
            'benefits',
            'location',
            'title',
            'time_period',
            'status_old',
            'started_at',
            'finished_at',
            'recruitment_start_date',
            'recruitment_end_date',
            'reserve_recruitment',
            'reserve_recruitment_start_date',
            'reserve_recruitment_end_date',
            'action_ongoing',
            'constant_coop',
            'action_start_date',
            'action_end_date',
            'volunteers_limit',
        ]


class UserGalleryForm(forms.ModelForm):
    u"""Form used for changing user profile of user."""
    image = forms.ImageField(label=u"Wybierz grafikę")
    is_avatar = forms.BooleanField(
        label=u"Użyć jako avatar?",
        required=False,
    )

    class Meta(object):
        model = UserGallery
        fields = [
            'image',
        ]


class OrganizationGalleryForm(forms.ModelForm):
    u"""Form used for changing organization profiel."""
    path = forms.ImageField(label=u"Wybierz grafikę")
    organization = forms.ModelChoiceField(
        label=u"Dodaj do organizacji",
        queryset=Organization.objects.all()
    )
    is_main = forms.BooleanField(
        label=u"Użyj jako zdjęcie główne? ",
        required=False,
    )

    class Meta(object):
        model = OrganizationGallery
        fields = ['path', 'organization']

    def __init__(self, userprofile, *args, **kwargs):
        u"""Initialize OrganizationGalleryForm object."""
        super(OrganizationGalleryForm, self).__init__(*args, **kwargs)
        self._set_user_organizations(userprofile)

    def _set_user_organizations(self, userprofile):
        u"""Get current user organizations."""
        self.fields['organization'].queryset = Organization.objects.filter(
            userprofiles=userprofile
        )


class OfferImageForm(forms.ModelForm):
    u"""Form used for upload offer image."""
    path = forms.ImageField(label=u"Dodaj zdjęcie")
    is_main = forms.BooleanField(
        label=u"Użyj jako zdjęcie główne? ",
        required=False,
    )

    class Meta(object):
        model = OfferImage
        fields = [
            'path',
        ]


class OfferApplyForm(forms.Form):
    u"""Form for applying for join to offer ."""

    email = forms.CharField(max_length=80)
    phone_no = forms.CharField(max_length=80)
    fullname = forms.CharField(max_length=80)
    comments = forms.CharField(required=False, widget=forms.Textarea)


class ContactForm(forms.Form):
    u"""Basic contact form."""

    email = forms.CharField(max_length=150)
    message = forms.CharField(widget=forms.Textarea())
    name = forms.CharField(max_length=150)
    phone_no = forms.CharField(max_length=150)


class VolounteerToOrganizationContactForm(ContactForm):
    U"""Contact form specified for volounteers to mail to organization."""
    organization = forms.CharField(widget=forms.HiddenInput())


class AdministratorContactForm(ContactForm):
    U"""Contact form specified for anyone to mail to administrator."""
    APPLICANTS = (
        ('VOLUNTEER', u'wolontariusz'),
        ('ORGANIZATION', u'organizacja'),
    )
    ADMINISTRATORS = [
        (key, value) for key, value in get_administrators_emails().items()
    ]
    applicant = forms.Select(choices=APPLICANTS)
    administrator = forms.Select(choices=ADMINISTRATORS)
