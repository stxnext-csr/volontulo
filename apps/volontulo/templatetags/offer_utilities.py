# -*- coding: utf-8 -*-

u"""
.. module:: offer_utilities
"""

from django import template

register = template.Library()


@register.filter(name='can_edit_offer')
def can_edit_offer(userprofile, offer):
    u"""Return whether the user can edit an offer based on an ID."""
    if userprofile is None:
        return False
    return userprofile.can_edit_offer(offer=offer)
