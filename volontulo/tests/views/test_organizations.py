# -*- coding: utf-8 -*-

u"""
.. module:: test_organizations
"""
from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from volontulo.models import Organization
from volontulo.models import UserProfile


class TestOrganizations(TestCase):
    u"""Class responsible for testing organization specific views."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        TestOrganizations.initialize_empty_organizations()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    @staticmethod
    def initialize_empty_organizations():
        u"""Initialize empty organization."""
        for i in range(1, 6):
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

    # pylint: disable=invalid-name
    def test__organization_list(self):
        u"""Test getting organization list as anonymous"""
        response = self.client.get('/organizations', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organizations/list.html')
        # pylint: disable=no-member
        self.assertIn('organizations', response.context)
        self.assertEqual(Organization.objects.all().count(), 5)
