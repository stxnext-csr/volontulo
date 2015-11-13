# -*- coding: utf-8 -*-

u"""
.. module:: offer_utilities
"""

from django import template

register = template.Library()  # pylint: disable=invalid-name


@register.filter(name='can_edit_offer')
def can_edit_offer(userprofile, offer):
    u"""Return whether the user can edit a given offer."""
    return userprofile.can_edit_offer(offer)
