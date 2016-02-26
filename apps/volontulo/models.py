# -*- coding: utf-8 -*-

u"""
.. module:: models
"""
# pylint: disable=unused-import
import logging
import os
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F
from django.utils import timezone

# pylint: disable=invalid-name
logger = logging.getLogger('volontulo.models')


class Organization(models.Model):
    u"""Model that handles ogranizations/institutions."""
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        u"""Organization model string reprezentation."""
        return self.name


class OffersManager(models.Manager):
    u"""Offers Manager."""

    def get_active(self):
        u"""Return active offers."""
        return self.filter(
            offer_status='published',
            action_status__in=('ongoing', 'future'),
            recruitment_status__in=('open', 'supplemental'),
        ).all()

    def get_for_administrator(self):
        u"""Return all offers for administrator to allow management."""
        return self.filter(offer_status='unpublished').all()

    def get_weightened(self, count=10):
        u"""Return all published offers ordered by weight.

        :param count: Integer
        :return:
        """
        return self.filter(
            offer_status='published').order_by('weight')[:count]

    def get_archived(self):
        u"""Return archived offers."""
        return self.filter(
            offer_status='published',
            action_status__in=('ongoing', 'finished'),
            recruitment_status='closed',
        ).all()


class Offer(models.Model):
    u"""Offer model."""

    OFFER_STATUSES = (
        ('unpublished', u'Unpublished'),
        ('published', u'Published'),
        ('rejected', u'Rejected'),
    )
    RECRUITMENT_STATUSES = (
        ('open', u'Open'),
        ('supplemental', u'Supplemental'),
        ('closed', u'Closed'),
    )
    ACTION_STATUSES = (
        ('future', u'Future'),
        ('ongoing', u'Ongoing'),
        ('finished', u'Finished'),
    )

    objects = OffersManager()
    organization = models.ForeignKey(Organization)
    volunteers = models.ManyToManyField(User)
    description = models.TextField()
    requirements = models.TextField(blank=True, default='')
    time_commitment = models.TextField()
    benefits = models.TextField()
    location = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    time_period = models.CharField(max_length=150, default='', blank=True)
    status_old = models.CharField(
        max_length=30,
        default='NEW',
        null=True,
        unique=False
    )
    offer_status = models.CharField(
        max_length=16,
        choices=OFFER_STATUSES,
        default='unpublished',
    )
    recruitment_status = models.CharField(
        max_length=16,
        choices=RECRUITMENT_STATUSES,
        default='open',
    )
    action_status = models.CharField(
        max_length=16,
        choices=ACTION_STATUSES,
        default='ongoing',
    )
    votes = models.BooleanField(default=0)
    recruitment_start_date = models.DateTimeField(blank=True, null=True)
    recruitment_end_date = models.DateTimeField(blank=True, null=True)
    reserve_recruitment = models.BooleanField(blank=True, default=True)
    reserve_recruitment_start_date = models.DateTimeField(
        blank=True,
        null=True
    )
    reserve_recruitment_end_date = models.DateTimeField(
        blank=True,
        null=True
    )
    action_ongoing = models.BooleanField(default=False, blank=True)
    constant_coop = models.BooleanField(default=False, blank=True)
    action_start_date = models.DateTimeField(blank=True, null=True)
    action_end_date = models.DateTimeField(blank=True, null=True)
    volunteers_limit = models.IntegerField(default=0, null=True, blank=True)
    weight = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        u"""Offer string representation."""
        return self.title

    def set_main_image(self, is_main):
        u"""Set main image flag unsetting other offers images.

        :param is_main: Boolean flag resetting offer main image
        """
        if is_main:
            OfferImage.objects.filter(offer=self).update(is_main=False)
            return True
        return False

    def save_offer_image(self, gallery, userprofile, is_main=False):
        u"""Handle image upload for user profile page.

        :param gallery: UserProfile model instance
        :param userprofile: UserProfile model instance
        :param is_main: Boolean main image flag
        """
        gallery.offer = self
        gallery.userprofile = userprofile
        gallery.is_main = self.set_main_image(is_main)
        gallery.save()
        return self

    def create_new(self):
        u"""Set status while creating new offer."""
        self.offer_status = 'unpublished'
        self.recruitment_status = 'open'

        if self.started_at or self.finished_at:
            self.action_status = self.determine_action_status()


    def determine_action_status(self):
        u"""Determine action status by offer dates."""
        if (
                (
                    self.finished_at and
                    self.started_at < timezone.now() < self.finished_at
                ) or
                (
                    self.started_at < timezone.now() and
                    not self.finished_at
                )
        ):
            return 'ongoing'
        elif self.started_at > timezone.now():
            return 'future'
        else:
            return 'finished'

    def change_status(self, status):
        u"""Change offer status.

        :param status: string Offer status
        """
        if status in ('published', 'rejected', 'unpublished'):
            self.offer_status = status
            self.save()
        return self

    def unpublish(self):
        u"""Unpublish offer."""
        self.offer_status = 'unpublished'
        self.save()
        return self

    def publish(self):
        u"""Publish offer."""
        self.offer_status = 'published'
        Offer.objects.all().update(weight=F('weight') + 1)
        self.weight = 0
        self.save()
        return self

    def reject(self):
        u"""Reject offer."""
        self.offer_status = 'rejected'
        self.save()
        return self

    def close_offer(self):
        u"""Change offer status to close."""
        self.offer_status = 'unpublished'
        self.action_status = 'finished'
        self.recruitment_status = 'closed'
        self.save()
        return self


class UserProfile(models.Model):
    u"""Model that handles users' profiles."""

    user = models.OneToOneField(User)
    organizations = models.ManyToManyField(
        Organization,
        related_name='userprofiles',
    )
    is_administrator = models.BooleanField(default=False, blank=True)
    phone_no = models.CharField(
        max_length=32,
        blank=True,
        default='',
        null=True
    )
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def is_admin(self):
        u"""Return True if current user is administrator, else return False"""
        return self.is_administrator

    def is_volunteer(self):
        u"""Return True if current user is volunteer, else return False"""
        return not (self.is_administrator and self.organizations)

    def can_edit_offer(self, offer=None, offer_id=None):
        u"""Checks if the user can edit an offer based on its ID"""
        if offer is None:
            offer = Offer.objects.get(id=offer_id)
        return self.is_administrator or self.organizations.filter(
            id=offer.organization_id).exists()

    def get_avatar(self):
        u"""Return avatar for current user."""
        return UserGallery.objects.filter(
            userprofile=self,
            is_avatar=True
        )

    def clean_images(self):
        u"""Clean user images."""
        images = UserGallery.objects.filter(userprofile=self)
        for image in images:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(image.image)))
            except OSError as ex:
                logger.error(ex)

            image.delete()

    def __str__(self):
        return self.user.email


class UserGallery(models.Model):
    u"""Handling user images."""
    userprofile = models.ForeignKey(UserProfile, related_name='images')
    image = models.ImageField(upload_to='profile/')
    is_avatar = models.BooleanField(default=False)

    def __str__(self):
        u"""String representation of an image."""
        return str(self.image)


class OfferImage(models.Model):
    u"""Handling offer image."""
    userprofile = models.ForeignKey(UserProfile, related_name='offerimages')
    offer = models.ForeignKey(Offer, related_name='images')
    path = models.ImageField(upload_to='offers/')
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        u"""String representation of an image."""
        return str(self.path)


class OrganizationGallery(models.Model):
    u"""Handling organizations gallery."""
    organization = models.ForeignKey(Organization, related_name='images')
    published_by = models.ForeignKey(UserProfile, related_name='gallery')
    path = models.ImageField(upload_to='gallery/')
    is_main = models.BooleanField(default=False, blank=True)

    def __str__(self):
        u"""String representation of an image."""
        return str(self.path)

    def remove(self):
        u"""Remove image."""
        self.remove()

    def set_as_main(self, organization):
        u"""Save image as main.

        :param organization: Organization model instance
        """
        OrganizationGallery.objects.filter(organization_id=organization.id)\
            .update(
                is_main=False
            )
        self.is_main = True
        self.save()

    @staticmethod
    def get_organizations_galleries(userprofile):
        u"""Get images grouped by organizations

        :param userprofile: UserProfile model instance
        """
        organizations = Organization.objects.filter(
            userprofiles=userprofile
        ).all()
        return {o.name: o.images.all() for o in organizations}
