# -*- coding: utf-8 -*-
u"""
.. module:: utils
"""

# class Utils:
#     u"""Utils module for volontulo application."""
from django.contrib.auth.models import User
from volontulo.models import UserProfile


def get_administrators_emails():
    u"""Get all administrators emails or superuser email

    Format returned:
    emails = {
        1: 'admin1@example.com',
        2: 'admin2@example.com',
    }
    """
    administrators = UserProfile.objects.filter(is_administrator=True)
    emails = {}
    for admin in administrators:
        emails[str(admin.user.id)] = admin.user.email

    if not emails:
        administrators = User.objects.filter(is_superuser=True)
        for admin in administrators:
            emails[str(admin.id)] = admin.email

    return emails
