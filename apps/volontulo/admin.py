# -*- coding: utf-8 -*-

u"""
.. module:: admin
"""

from django.contrib import admin

from apps.volontulo.models import (
    UserProfile,
    Organization,
    Offer
)


admin.site.register(UserProfile)
admin.site.register(Organization)
admin.site.register(Offer)
