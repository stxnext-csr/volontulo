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
        # volunteer user - badges, offers, organizations
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
