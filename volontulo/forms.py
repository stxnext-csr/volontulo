# -*- coding: utf-8 -*-

u"""
.. module:: forms
"""

from django import forms
from django.contrib.auth.models import User

from volontulo.models import Offer
from volontulo.models import UserProfile
from volontulo.utils import get_administrators_emails


class UserForm(forms.ModelForm):
    u"""Form reposponsible for authorization."""
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta(object):
        model = User
        fields = ['email']


class ProfileForm(forms.ModelForm):
    u"""Form used for changing profile of user."""
    is_organization = forms.BooleanField(required=False)

    class Meta(object):
        model = UserProfile
        fields = ['is_organization']


class CreateOfferForm(forms.ModelForm):
    u"""Form reposponsible for creating offer by organization."""

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


class OfferApplyForm(forms.Form):
    u"""Form for applying for join to offer ."""

    email = forms.CharField(max_length=80)
    phone_no = forms.CharField(max_length=80)
    fullname = forms.CharField(max_length=80)
    comments = forms.CharField(widget=forms.Textarea, max_length=80)


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
