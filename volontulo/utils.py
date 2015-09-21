# -*- coding: utf-8 -*-

u"""
.. module:: utils
"""
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

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


def save_history(req, obj, action):
    u"""Save model changes history."""
    LogEntry.objects.log_action(
        user_id=req.user.pk,
        content_type_id=ContentType.objects.get_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=action
    )
