# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from volontulo.models import Offer
from volontulo.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta(object):
        model = User
        fields = ['email']


class ProfileForm(forms.ModelForm):
    is_organization = forms.BooleanField()

    class Meta(object):
        model = UserProfile
        fields = ['is_organization']


class CreateOfferForm(forms.ModelForm):

    class Meta(object):
        model = Offer
        fields = [
            'description',
            'requirements',
            'time_commitment',
            'benefits',
            'location',
            'title',
            'time_period',
            'status',
        ]
