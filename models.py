# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Offer(models.Model):
    organization = models.ForeignKey(Organization)
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

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    is_organization = models.BooleanField(default=False, blank=True)
    is_administrator = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.user.email
