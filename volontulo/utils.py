# -*- coding: utf-8 -*-

u"""
.. module:: utils
"""

from django.contrib.auth.models import User

from volontulo.models import UserProfile


def get_administrators_emails():
    u"""Get all administrators emails or superuser email."""
    administrators = UserProfile.objects.filter(is_administrator=True)
    emails = []
    for admin in administrators:
        emails.append(admin.user.email)

    if not emails:
        administrators = User.objects.filter(is_superuser=True)
        for admin in administrators:
            emails.append(admin.user.email)

    return emails
