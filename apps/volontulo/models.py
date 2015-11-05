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

    VISIBILITY_MATRIX = {
        ('unpublished', 'open', 'future'): 0,
        ('unpublished', 'open', 'ongoing'): 0,
        ('unpublished', 'open', 'finished'): 0,
        ('unpublished', 'supplemental', 'future'): 0,
        ('unpublished', 'supplemental', 'ongoing'): 0,
        ('unpublished', 'supplemental', 'finished'): 0,
        ('unpublished', 'closed', 'future'): 0,
        ('unpublished', 'closed', 'ongoing'): 0,
        ('unpublished', 'closed', 'finished'): 0,
        ('published', 'open', 'future'): 1,
        ('published', 'open', 'ongoing'): 1,
        ('published', 'open', 'finished'): 0,
        ('published', 'supplemental', 'future'): 1,
        ('published', 'supplemental', 'ongoing'): 1,
        ('published', 'supplemental', 'finished'): 0,
        ('published', 'closed', 'future'): 1,
        ('published', 'closed', 'ongoing'): 0,
        ('published', 'closed', 'finished'): 1,
        ('rejected', 'open', 'future'): 1,
        ('rejected', 'open', 'ongoing'): 1,
        ('rejected', 'open', 'finished'): 1,
        ('rejected', 'supplemental', 'future'): 1,
        ('rejected', 'supplemental', 'ongoing'): 1,
        ('rejected', 'supplemental', 'finished'): 0,
        ('rejected', 'closed', 'future'): 0,
        ('rejected', 'closed', 'ongoing'): 0,
        ('rejected', 'closed', 'finished'): 0,
    }

    objects = OffersManager()
    organization = models.ForeignKey(Organization)
    volunteers = models.ManyToManyField(User)
    description = models.TextField()
    requirements = models.TextField()
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

    def __str__(self):
        return self.title

    def is_visible(self):
        u"""Determine offer visibility for specified user type."""
        statuses_keys = (
            self.offer_status,
            self.recruitment_status,
            self.action_status
        )
        return True if self.VISIBILITY_MATRIX[statuses_keys] else False

    def set_main_image(self, form):
        u"""Set main image flag unsetting other offers images.

        :param offer: Offer model instance
        """
        if form.cleaned_data["is_main"]:
            OfferImage.objects.filter(offer=self).update(is_main=False)
            return True
        return False

    def save_offer_image(self, form, userprofile):
        u"""Handle image upload for user profile page.

        :param offer: Offer model instance
        """
        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.offer = self
            gallery.userprofile = userprofile
            gallery.is_main = self.set_main_image(form)
            gallery.save()
            return True
        else:
            return form.errors

    def create_new(self):
        u"""Set status while creating new offer."""
        self.offer_status = 'unpublished'
        self.recruitment_status = 'open'
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

    def change_status(self, request):
        u"""Change offer status.

        :param offer: Offer model instance
        """
        if request.POST.get('status') in {'published', 'rejected'}:
            self.offer_status = request.POST.get('status')
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

#     def open_recruitment(self):
#         u"""Change recruitation status of current offer open."""
#         self.recruitment_status = 'open'
#         return self
#
#     def close_recruitment(self):
#         u"""Change recruitation status of current offer closed."""
#         self.recruitment_status = 'closed'
#         return self
#
#     def supplement_recruitment(self):
#         u"""Change recruitation status of current offer supplemental."""
#         self.recruitment_status = 'supplemental'
#         return self
#
#     def futured_action(self):
#         u"""Change state of current offer to publish."""
#         self.action_status = 'future'
#         return self
#
#     def ongoing_action(self):
#         u"""Change state of current offer to unpublished."""
#         self.action_status = 'ongoing'
#         return self
#
#     def finished_action(self):
#         u"""Change state of current offer to rejected."""
#         self.action_status = 'finished'
#         return self


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


class OfferImage(models.Model):
    u"""Handling offer image."""
    userprofile = models.ForeignKey(UserProfile, related_name='offerimages')
    offer = models.ForeignKey(Offer)
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
