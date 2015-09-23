# -*- coding: utf-8 -*-

u"""
.. module:: email
"""

from django.core.mail import EmailMultiAlternatives
from django.core.mail import get_connection
from django.template import Context
from django.template.loader import get_template

from volontulo.utils import get_administrators_emails

FROM_ADDRESS = 'support@volontuloapp.org'
FAIL_SILENTLY = False
AUTH_USER = None
AUTH_PASSWORD = None
CONNECTION = None

SUBJECTS = {
    'offer_application': u'Zgłoszenie chęci pomocy w ofercie',
    'offer_creation': u'Zgłoszenie oferty na Volontulo',
    'registration': u'Rejestracja na Volontulo',
    'volunteer_to_admin': u'Kontakt z administratorem',
    'volunteer_to_organisation': u'Kontakt od wolontariusza',
}


# pylint: disable=unused-argument
def send_mail(templates_name, recipient_list, context=None):
    u"""Proxy for sending emails."""

    fail_silently = FAIL_SILENTLY
    auth_user = AUTH_USER
    auth_password = AUTH_PASSWORD
    connection = CONNECTION

    context = Context(context or {})
    text_template = get_template('emails/{}.txt'.format(templates_name))
    html_template = get_template('emails/{}.html'.format(templates_name))

    bcc = list(get_administrators_emails().values())
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently
    )
    # required, if omitted then no emails from BCC are send
    headers = {'bcc': ','.join(bcc)}
    email = EmailMultiAlternatives(
        SUBJECTS[templates_name],
        text_template.render(context),
        FROM_ADDRESS,
        recipient_list,
        bcc,
        connection=connection,
        headers=headers
    )
    email.attach_alternative(html_template.render(context), 'text/html')

    return email.send()
