# -*- coding: utf-8 -*-

u"""
.. module:: email
"""

from django.core.mail import send_mail as django_send_mail


FROM_ADDRESS = 'support@volontuloapp.org'


def send_mail(subject, message, recipient_list, html_message=None):
    return django_send_mail(
        subject,
        message,
        FROM_ADDRESS,
        recipient_list,
        fail_silently=False,
        html_message=html_message,
    )
