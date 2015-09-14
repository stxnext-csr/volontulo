# -*- coding: utf-8 -*-

from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=150)


class Offer(models.Model):
    organization = models.ForeignKey(Organization)
    description = models.TextField()
    requirements = models.TextField()
    time_commitment = models.TextField()
    benefits = models.TextField()
    location = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    time_period = models.CharField(max_length=150)
