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
from django.utils import timezone

# pylint: disable=invalid-name
logger = logging.getLogger('volontulo.models')


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
    status_old = models.CharField(max_length=30, default='NEW')
    votes = models.BooleanField(default=0)

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
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def is_admin(self):
        u"""Return True if current user is administrator, else return False"""
        return self.is_administrator

    def is_volunteer(self):
        u"""Return True if current user is volunteer, else return False"""
        return not (self.is_administrator and self.organizations)

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


class UserBadges(models.Model):
    u"""Users to bages relation table."""
    userprofile = models.ForeignKey(UserProfile, db_column='userprofile_id')
    badge = models.ForeignKey(Badge)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    description = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, null=True)
    counter = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.description

    @staticmethod
    def get_user_badges(userprofile):
        u"""Return User badges for selected user."""
        return UserBadges.objects \
            .filter(userprofile=userprofile.id) \
            .values('badge_id', 'badge__name', 'badge__priority') \
            .annotate(badges=models.Count('badge_id')) \
            .order_by('-badge__priority')

    @staticmethod
    def apply_participant_badge(content_type, volunteer_user):
        u"""Helper function to apply particpant badge to specified user."""

        participant_badge = Badge.objects.get(slug='participant')
        try:
            usersbadge = UserBadges.objects.get(
                userprofile=volunteer_user,
                badge=participant_badge,
                content_type=content_type,
            )
            usersbadge.counter += 1
            usersbadge.save()
        except UserBadges.DoesNotExist:
            UserBadges.objects.create(
                userprofile=volunteer_user,
                badge=participant_badge,
                content_type=content_type,
                created_at=timezone.now(),
                description=u"Wolontariusz {} - 'Uczestnik'.".format(
                    volunteer_user.user.email
                ),
                counter=1
            )

    @staticmethod
    # pylint: disable=invalid-name
    def apply_prominent_participant_badge(content_type, volunteer_user):
        u"""Helper function to apply particpant badge to specified user."""
        badge = Badge.objects.get(slug='prominent-participant')
        try:
            usersbadge = UserBadges.objects.get(
                userprofile=volunteer_user,
                badge=badge,
                content_type=content_type,
            )
            usersbadge.counter += 1
            usersbadge.save()
        except UserBadges.DoesNotExist:
            UserBadges.objects.create(
                userprofile=volunteer_user,
                badge=badge,
                content_type=content_type,
                created_at=timezone.now(),
                description=u"Wolontariusz {} - 'Wybitny uczestnik'.".format(
                    volunteer_user.user.email
                ),
                counter=1
            )
        finally:
            UserBadges.decrease_user_participant_badge(
                content_type,
                volunteer_user
            )

    @staticmethod
    def decrease_user_participant_badge(content_type, volunteer_user):
        u"""Helper function to decrease users participant badge."""

        badge = Badge.objects.get(slug='participant')
        try:
            usersbadge = UserBadges.objects.get(
                userprofile=volunteer_user,
                badge=badge,
                content_type=content_type,
            )
            if usersbadge.counter == 1:
                usersbadge.delete()
            else:
                usersbadge.counter -= 1
                usersbadge.save()
        except UserBadges.DoesNotExist:
            # innocent user does not have any participant badge
            pass


class UserGallery(models.Model):
    u"""Handling user images."""
    userprofile = models.ForeignKey(UserProfile, related_name='images')
    image = models.ImageField(upload_to='profile/')
    is_avatar = models.BooleanField(default=False)

    def __str__(self):
        u"""String representation of an image."""
        return str(self.image)


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
        u"""Save image as main."""
        OrganizationGallery.objects.filter(organization_id=organization.id)\
            .update(
                is_main=False
            )
        self.is_main = True
        self.save()

    @staticmethod
    def get_organizations_galleries(userprofile):
        u"""Get images grouped by organizations"""
        organizations = Organization.objects.filter(
            userprofiles=userprofile
        ).all()
        return {o.name: o.images.all() for o in organizations}
