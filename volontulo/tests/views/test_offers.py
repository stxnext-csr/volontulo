# -*- coding: utf-8 -*-

u"""
.. module:: test_offers
"""

from django.test import Client
from django.test import TestCase

from volontulo.models import Offer
from volontulo.models import Organization


class TestOffersList(TestCase):
    u"""Class responsible for testing offers' list."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        cls.organization = Organization.objects.create(
            name=u'',
            address=u'',
            description=u'',
        )
        cls.organization.save()

        common_offer_data = {
            'organization': cls.organization,
            'description': u'',
            'requirements': u'',
            'time_commitment': u'',
            'benefits': u'',
            'location': u'',
            'title': u'volontulo offer',
            'time_period': u''
        }

        cls.inactive_offer = Offer.objects.create(
            status='NEW',
            **common_offer_data
        )
        cls.inactive_offer.save()
        cls.active_offer = Offer.objects.create(
            status='ACTIVE',
            **common_offer_data
        )
        cls.active_offer.save()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    # pylint: disable=invalid-name
    def test_offers_list_for_anonymous_user(self):
        u"""Test offers' list for anonymous user.

        List of offers is available for anonymous users and shows only ACTIVE
        offers.
        """
        response = self.client.get('/offers')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offers_list.html')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        # pylint: disable=no-member
        self.assertEqual(len(response.context['offers']), 1)
