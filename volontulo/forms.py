# -*- coding: utf-8 -*-

u"""
.. module:: forms
"""
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# from volontulo.models import EditProfile
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

    # class Meta(object):
    #     model = EditProfile

    def is_valid(self):
        super(EditProfileForm, self).is_valid()
        if self.current_password != User.objects.get(user=1):
            raise ValidationError("Current password is incorrect.")

        if self.new_password != self.confirm_new_password:
            raise ValidationError("Confirmation password doesn't match.")


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
    image = forms.FileField(label=u"Wybierz grafikę")

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
