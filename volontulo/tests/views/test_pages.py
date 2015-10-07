# -*- coding: utf-8 -*-

u"""
.. module:: test_pages
"""
from django.test import Client
from django.test import TestCase

from volontulo.tests.common import Common


class TestPages(TestCase):
    u"""Class responsible for testing various pages."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        Common.initialize_filled_volunteer_and_organization()
        Common.initialize_administrator()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    def test__homepage_for_anonymous(self):
        u"""Home page for anonymous users."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        # pylint: disable=no-member
        self.assertEqual(len(response.context['offers']), 4)

    # pylint: disable=invalid-name
    def test__homepage_for_volunteer_and_organization(self):
        u"""Home page for volunteers and organizations.

            There's currently no difference for anonymous
            or volunteer/organization - for now.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        # pylint: disable=no-member
        self.assertEqual(len(response.context['offers']), 4)

    # pylint: disable=invalid-name
    def test__homepage_for_administrator(self):
        u"""Home page for administrators."""
        self.client.post('/login', {
            'email': u'administrator1@example.com',
            'password': 'administrator1',
        })
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/list_offers.html')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        # pylint: disable=no-member
        self.assertEqual(len(response.context['offers']), 14)

        offers = {u'NEW': 0, u'ACTIVE': 0, u'SUSPENDED': 0}
        for offer in response.context['offers']:
            offers[offer.status] += 1

        self.assertEqual(offers[u'ACTIVE'], 4)
        self.assertEqual(offers[u'NEW'], 5)
        self.assertEqual(offers[u'SUSPENDED'], 5)
