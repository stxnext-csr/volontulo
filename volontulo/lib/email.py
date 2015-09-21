# -*- coding: utf-8 -*-

u"""
.. module:: email
"""

from django.core.mail import send_mail as django_send_mail
from django.template import Context
from django.template.loader import get_template


FROM_ADDRESS = 'support@volontuloapp.org'

SUBJECTS = {
    'offer_application': u'Zgłoszenie chęci pomocy w ofercie',
    'offer_creation': u'Zgłoszenie oferty na Volontulo',
    'registration': u'Rejestracja na Volontulo',
    'volunteer_to_organisation': u'Kontakt od wolontariusza',
}


def send_mail(templates_name, recipient_list, context=None):
    u"""Proxy for sending emails."""
    context = Context(context or {})
    text_template = get_template('emails/{}.txt'.format(templates_name))
    html_template = get_template('emails/{}.html'.format(templates_name))

    return django_send_mail(
        SUBJECTS[templates_name],
        text_template.render(context),
        FROM_ADDRESS,
        recipient_list,
        fail_silently=False,
        html_message=html_template.render(context),
    )
