# -*- coding: utf-8 -*-

u"""
.. module:: test_organizations
"""
from django.test import Client
from django.test import TestCase

from apps.volontulo.models import Organization
from apps.volontulo.tests import common


class TestOrganizations(TestCase):
    u"""Class responsible for testing organization specific views."""

    @classmethod
    def setUpTestData(cls):
        u"""Data fixtures for all tests."""
        # volunteer user - totally useless
        cls.volunteer = common.initialize_empty_volunteer()
        # organization user - no offers
        cls.organization = common.initialize_empty_organization()
        # volunteer user - offers, organizations
        cls.volunteer2, cls.organization2 = \
            common.initialize_filled_volunteer_and_organization()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    # pylint: disable=invalid-name
    def test__organization_list(self):
        u"""Test getting organization list as anonymous."""
        response = self.client.get('/organizations', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organizations/list.html')
        # pylint: disable=no-member
        self.assertIn('organizations', response.context)
        self.assertEqual(Organization.objects.all().count(), 2)

    # pylint: disable=invalid-name
    def test__ensure_status_is_displayed_in_profile_view(self):
        """Test if offer status is displayed in a profile view."""
        self.client.login(
            username=u'volunteer2@example.com',
            password=u'volunteer2'
        )
        response = self.client.get('/me', follow=True)
        self.assertTemplateUsed(response, 'users/my_offers.html')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        # pylint: disable=no-member
        self.assertEquals(
            'published', response.context['offers'][0].offer_status)

    # pylint: disable=invalid-name
    def test__ensure_status_is_displayed_in_organisations_view(self):
        """Test if offer status is displayed in an organisation view."""
        self.client.login(
            username=u'volunteer2@example.com',
            password=u'volunteer2'
        )
        response = self.client.get('/me', follow=True)
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        # pylint: disable=no-member
        self.assertEquals(
            'published', response.context['offers'][0].offer_status)
