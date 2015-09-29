# -*- coding: utf-8 -*-

u"""
.. module:: models
"""

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Organization(models.Model):
    u"""Model that handles ogranizations/institutions."""
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name


class Offer(models.Model):
    u"""Model that hadles offers."""
    organization = models.ForeignKey(Organization)
    volunteers = models.ManyToManyField(User)
    description = models.TextField()
    requirements = models.TextField()
    time_commitment = models.TextField()
    benefits = models.TextField()
    location = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    time_period = models.CharField(max_length=150)
    status = models.CharField(max_length=30, default='STAGED')

    def __str__(self):
        return self.title


class Badge(models.Model):
    u"""Generic badge representation."""
    name = models.CharField(max_length=150)
    priority = models.IntegerField(default=1)

    def __init__(self, name, priority=1, *args, **kwargs):
        u"""Initialize default badge."""
        super(Badge, self).__init__(*args, **kwargs)
        self.name = name
        self.priority = priority

    def __str__(self):
        u"""Badge string representation."""
        return self.name


class UserProfile(models.Model):
    u"""Model that handles users' profiles."""
    user = models.OneToOneField(User)
    organizations = models.ManyToManyField(
        Organization,
        related_name='userprofiles',
    )
    is_administrator = models.BooleanField(default=False, blank=True)
    badges = models.ManyToManyField(
        'Badge',
        through='UserBadges',
        related_name='user_profile'
    )

    def __str__(self):
        return self.user.email


class UserBadges(models.Model):
    u"""Users to bages relation table."""
    user = models.ForeignKey(UserProfile)
    badge = models.ForeignKey(Badge)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description
