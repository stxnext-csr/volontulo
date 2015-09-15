# -*- coding: utf-8 -*-

u"""
.. module:: admin
"""

from django.contrib import admin

from volontulo.models import UserProfile


admin.site.register(UserProfile)
