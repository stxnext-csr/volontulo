# -*- coding: utf-8 -*-

u"""
.. module:: labeled_status
"""

from django import template

from volontulo.utils import offer_statuses


register = template.Library()  # pylint: disable=invalid-name


@register.filter(name='human')
def human(status):
    u"""Get offer status description."""
    statuses = offer_statuses()
    return statuses.get(status, status)
