# -*- coding: utf-8 -*-

u"""
.. module:: models
"""

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    u"""Model that handles users' profiles."""
    user = models.OneToOneField(User)
    is_admin = models.BooleanField()


class Organization(models.Model):
    u"""Model that handles organizacions/institutions."""
    name = models.CharField(max_length=150)


class Offer(models.Model):
    u"""Model that hadles offers."""
    organization = models.ForeignKey(Organization)
    description = models.TextField()
    requirements = models.TextField()
    time_commitment = models.TextField()
    benefits = models.TextField()
    location = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    time_period = models.CharField(max_length=150)
    status = models.CharField(max_length=30, default='STAGED')
