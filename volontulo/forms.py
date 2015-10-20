# -*- coding: utf-8 -*-

u"""
.. module:: forms
"""
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from volontulo.models import Offer
from volontulo.models import UserGallery
from volontulo.utils import get_administrators_emails


class UserForm(forms.ModelForm):
    u"""Form reposponsible for authorization."""
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta(object):
        model = User
        fields = ['email']


class EditProfileForm(forms.Form):
    u"""Form reposponsible for edit user details on profile page."""
    email = forms.EmailField(label="Email")
    current_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(widget=forms.PasswordInput())
    user = forms.CharField(widget=forms.HiddenInput())

    def is_valid(self):
        valid = super(EditProfileForm, self).is_valid()
        if not valid:
            return valid

        current_password = self.cleaned_data['current_password']
        user = User.objects.get(id=self.cleaned_data['user'])

        if not user.check_password(current_password):
            raise ValidationError(u"Aktualne hasło jest błędne")

        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']
        if new_password:
            if new_password != confirm_new_password:
                raise ValidationError(u"Wprowadzone hasła różnią się")
        else:
            raise ValidationError(u"Nowe hasło nie może być puste.")

        return True


class CreateOfferForm(forms.ModelForm):
    u"""Form reposponsible for creating offer by organization."""

    def __init__(self, *args, **kwargs):
        super(CreateOfferForm, self).__init__(*args, **kwargs)
        self.fields['status'].required = False

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
            'status',
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


class OfferApplyForm(forms.Form):
    u"""Form for applying for join to offer ."""

    email = forms.CharField(max_length=80)
    phone_no = forms.CharField(max_length=80)
    fullname = forms.CharField(max_length=80)
    comments = forms.CharField(widget=forms.Textarea)


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
