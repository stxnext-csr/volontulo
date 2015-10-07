# -*- coding: utf-8 -*-

u"""
.. module:: common
"""

from django.contrib.auth.models import User

from volontulo.models import Badge
from volontulo.models import Offer
from volontulo.models import Organization
from volontulo.models import UserBadges
from volontulo.models import UserProfile


class Common(object):
    u"""Handle helper methods used in many places."""

    @staticmethod
    def initialize_empty_volunteer():
        u"""Initialize empty volunteer."""
        volunteer_user1 = User.objects.create_user(
            'volunteer1@example.com',
            'volunteer1@example.com',
            'volunteer1'
        )
        volunteer_user1.save()
        UserProfile.objects.create(user=volunteer_user1)

    @staticmethod
    def initialize_empty_organization():
        u"""Initialize empty organization."""
        organization1 = Organization.objects.create(name=u'Organization 1')
        organization1.save()
        organization_user1 = User.objects.create_user(
            'organization1@example.com',
            'organization1@example.com',
            'organization1'
        )
        organization_user1.save()
        organization_profile1 = UserProfile.objects.create(
            user=organization_user1,
        )
        organization_profile1.organizations.add(organization1)

    @staticmethod
    # pylint: disable=invalid-name
    def initialize_filled_volunteer_and_organization():
        u"""Initialize volunteer filled with data."""
        # create volunteer user
        volunteer_user2 = User.objects.create_user(
            'volunteer2@example.com',
            'volunteer2@example.com',
            'volunteer2'
        )
        volunteer_user2.save()
        user_profile2 = UserProfile.objects.create(user=volunteer_user2)

        # create 3 badges with different priorities
        for i in range(1, 4):
            badge = Badge.objects.create(
                name='Badge {}'.format(i),
                slug='badge-{}'.format(i),
                priority=i,
            )
            badge.save()
            usersbadge = UserBadges.objects.create(
                userprofile=user_profile2,
                badge=badge,
                counter=i,
            )
            usersbadge.save()

        # create organization user to create offers
        organization2 = Organization.objects.create(name=u'Organization 2')
        organization2.save()
        # this is required due to login to this user
        organization_user2 = User.objects.create_user(
            'organization2@example.com',
            'organization2@example.com',
            'organization2'
        )
        organization_user2.save()
        organization_profile2 = UserProfile.objects.create(
            user=organization_user2,
        )
        organization_profile2.organizations.add(organization2)

        # create organization offers and assign volunteer to them
        for i in range(11, 15):
            offer = Offer.objects.create(
                title=u'Title {}'.format(i),
                description=u'Description {}'.format(i),
                requirements=u'Requirements {}'.format(i),
                time_commitment=u'Time commitment {}'.format(i),
                benefits=u'Benefits {}'.format(i),
                location=u'Location {}'.format(i),
                time_period=u'Time period {}'.format(i),
                status=u'ACTIVE',
                votes=True,
                organization=organization2,
            )
            offer.volunteers.add(volunteer_user2)
            offer.save()

        # create additional organization offers for administrator use
        for i in range(100, 110):
            offer2 = Offer.objects.create(
                title=u'Title {}'.format(i),
                description=u'Description {}'.format(i),
                requirements=u'Requirements {}'.format(i),
                time_commitment=u'Time commitment {}'.format(i),
                benefits=u'Benefits {}'.format(i),
                location=u'Location {}'.format(i),
                time_period=u'Time period {}'.format(i),
                status=u'SUSPENDED' if i % 2 == 0 else u'NEW',
                votes=True,
                organization=organization2,
            )
            offer2.save()

    @staticmethod
    def initialize_empty_organizations():
        u"""Initialize empty organization."""
        for i in range(11, 15):
            organization = Organization.objects.create(
                name=u'Organization {}'.format(i)
            )
            organization.save()
            organization_user = User.objects.create_user(
                'organization{}@example.com'.format(i),
                'organization{}@example.com'.format(i),
                'organization{}'.format(i)
            )
            organization_user.save()
            user_profile = UserProfile.objects.create(
                user=organization_user,
            )
            user_profile.organizations.add(organization)

    @staticmethod
    def initialize_administrator():
        u"""Initialize administrator user."""
        administrator1 = User.objects.create_user(
            'administrator1@example.com',
            'administrator1@example.com',
            'administrator1'
        )
        administrator1.save()
        administrator_profile = UserProfile.objects.create(user=administrator1)
        administrator_profile.is_administrator = True
        administrator_profile.save()
