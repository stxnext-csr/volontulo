# -*- coding: utf-8 -*-

"""
.. module:: commons
"""

from django.contrib.auth.models import User

from apps.volontulo.models import Offer
from apps.volontulo.models import Organization
from apps.volontulo.models import UserProfile


# pylint: disable=too-few-public-methods
class TestOffersCommons(object):
    """Commons setups for offers' testcases."""

    # pylint: disable=invalid-name
    @classmethod
    def setUpTestData(cls):
        """Set up data for all tests."""
        cls.organization = Organization.objects.create(
            name='Organization Name',
            address='',
            description='',
        )
        cls.organization.save()

        cls.common_offer_data = {
            'organization': cls.organization,
            'description': '',
            'requirements': '',
            'time_commitment': '',
            'benefits': '',
            'location': '',
            'title': 'volontulo offer',
            'time_period': '',
            'started_at': '2105-10-24 09:10:11',
            'finished_at': '2105-11-28 12:13:14',
            'offer_status': 'unpublished',
            'recruitment_status': 'closed',
            'action_status': 'ongoing',
        }

        cls.inactive_offer = Offer.objects.create(
            status_old='NEW',
            **cls.common_offer_data
        )
        cls.inactive_offer.save()
        cls.active_offer = Offer.objects.create(
            status_old='ACTIVE',
            **cls.common_offer_data
        )
        cls.active_offer.save()

        volunteer_user = User.objects.create_user(
            'volunteer@example.com',
            'volunteer@example.com',
            '123volunteer'
        )

        cls.volunteer = UserProfile(user=volunteer_user)
        cls.volunteer.save()

        organization_user = User.objects.create_user(
            'cls.organization@example.com',
            'cls.organization@example.com',
            '123org'
        )

        cls.organization_profile = UserProfile(
            user=organization_user,
        )
        cls.organization_profile.save()
        # pylint: disable=no-member
        cls.organization_profile.organizations.add(cls.organization)

        admin_user = User.objects.create_user(
            'admin@example.com',
            'admin@example.com',
            '123admin'
        )

        cls.admin = UserProfile(
            user=admin_user,
            is_administrator=True,
        )
        cls.admin.save()
