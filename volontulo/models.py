# -*- coding: utf-8 -*-

u"""
.. module:: models
"""

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
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
    slug = models.CharField(max_length=150)
    priority = models.IntegerField(default=1)

    def __str__(self):
        u"""Badge string representation."""
        return self.name


class UserProfile(models.Model):
    u"""Model that handles users' profiles."""
    user = models.OneToOneField(User, related_name='userprofile')
    organization = models.ForeignKey(Organization, blank=True, null=True)
    is_administrator = models.BooleanField(default=False, blank=True)
    badges = models.ManyToManyField(
        'Badge',
        through='UserBadges',
        related_name='user_profile'
    )

    def is_admin(self):
        u"""Return True if current user is administrator, else return False"""
        return self.is_administrator

    def is_volunteer(self):
        u"""Return True if current user is volunteer, else return False"""
        return not (self.is_administrator and self.organization)

    def __str__(self):
        return self.user.email


class UserBadges(models.Model):
    u"""Users to bages relation table."""
    userprofile = models.ForeignKey(UserProfile, db_column='userprofile_id')
    badge = models.ForeignKey(Badge)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    description = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, null=True)

    def __str__(self):
        return self.description
