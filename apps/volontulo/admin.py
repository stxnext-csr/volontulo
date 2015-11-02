# -*- coding: utf-8 -*-

u"""
.. module:: admin
"""

from django.contrib import admin

from apps.volontulo.models import UserProfile


admin.site.register(UserProfile)
