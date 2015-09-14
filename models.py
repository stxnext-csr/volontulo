# -*- coding: utf-8 -*-

from django.db import models


class Organization(models.Model):
    pass


class Offer(models.Model):
    organization = models.ForeignKey(Organization)
    description = models.TextField()
    requirements = models.TextField()
    time_commitment = models.TextField()
    benefits = models.TextField()
