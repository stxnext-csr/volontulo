# -*- coding: utf-8 -*-

u"""
.. module:: labeled_status
"""

from django import template

from apps.volontulo.utils import OFFERS_STATUSES


register = template.Library()  # pylint: disable=invalid-name


@register.filter(name='human')
def human(status):
    u"""Get offer status description.

    :param status: string Status key
    """
    return OFFERS_STATUSES.get(status, status)
