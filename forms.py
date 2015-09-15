# -*- coding: utf-8 -*-

u"""
.. module:: forms
"""

from django import forms
from django.contrib.auth.models import User

from volontulo.models import UserProfile


class UserForm(forms.ModelForm):
    u"""Form reposponsible for authorization."""
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta(object):
        model = User
        fields = ['email']


class ProfileForm(forms.ModelForm):
    u"""Form used for changing profile of user."""

    class Meta(object):
        model = UserProfile
        fields = ['is_organization']
