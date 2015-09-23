# -*- coding: utf-8 -*-

u"""
.. module:: test_offers
"""

from django.test import Client
from django.test import TestCase


class TestOffersList(TestCase):
    u"""Class responsible for testing offers' list."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        pass

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
