# -*- coding: utf-8 -*-

u"""
.. module:: test_offers_2
"""

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from apps.volontulo.models import Offer
from apps.volontulo.models import Organization
from apps.volontulo.models import UserProfile


class TestOffersArchived(TestCase):
    """Class responsible for testing archived offers page."""

    @classmethod
    def setUpTestData(cls):
        """Set up data for all tests."""
        for i in range(1, 6):
            Organization.objects.create(
                name='Organization {0} name'.format(i),
                address='Organization {0} address'.format(i),
                description='Organization {0} description'.format(i),
            )

        organizations = Organization.objects.all()
        for idx, org in enumerate(organizations):
            for i in range(1, 6):
                user = User.objects.create_user(
                    'volunteer{0}{1}@example.com'.format(idx + 1, i),
                    'volunteer{0}{1}@example.com'.format(idx + 1, i),
                    'password',
                )
                userprofile = UserProfile(user=user)
                userprofile.save()
                userprofile.organizations.add(org)
                userprofile.save()

        for idx, org in enumerate(organizations):
            for i in range(0, idx + 1):
                Offer.objects.create(
                    organization=org,
                    benefits='Offer {0}-{1} benefits'.format(idx + 1, i),
                    location='Offer {0}-{1} location'.format(idx + 1, i),
                    title='Offer {0}-{1} title'.format(idx + 1, i),
                    time_period='',
                    description='',
                    requirements='',
                    time_commitment='',
                    offer_status='published',
                    recruitment_status='closed',
                    action_status='finished',
                    started_at='2010-10-10 10:10:10',
                    finished_at='2012-12-12 12:12:12'
                )

    def setUp(self):
        """Set up each test."""
        self.client = Client()

    def test_offers_archived_page(self):
        """Offers archive page."""
        response = self.client.get('/offers/archived')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/archived.html')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        self.assertEqual(len(response.context['offers']), 15)
        self.assertNotContains(
            response,
            'Brak ofert spełniających podane kryteria',
        )
