# -*- coding: utf-8 -*-

u"""
.. module:: test_userprofile
"""
from __future__ import unicode_literals
from django.test import TestCase

from apps.volontulo.models import Organization
from apps.volontulo.models import User
from apps.volontulo.models import UserProfile


class TestUserProfile(TestCase):
    u"""Class responsible for testing UserProfile model."""

    def setUp(self):
        u"""Set up each test."""

        # volunteer user
        self.volunteer_user = UserProfile.objects.create(
            user=User.objects.create_user(
                username='volunteer@example.com',
                email='volunteer@example.com',
                password='volunteer',
            ),
            is_administrator=False,
        )

        # organization user
        self.organization_user = UserProfile.objects.create(
            user=User.objects.create_user(
                username='organization@example.com',
                email='organization@example.com',
                password='organization',
            ),
            is_administrator=False,
        )
        self.organization_user.organizations.add(
            Organization.objects.create(name=u'Organization')
        )

        # administrator user
        self.administrator_user = UserProfile.objects.create(
            user=User.objects.create_user(
                username='administrator@example.com',
                email='administrator@example.com',
                password='administrator',
            ),
            is_administrator=True
        )

    def test__string_reprezentation(self):
        u"""String reprezentation of an userprofile object."""
        self.assertEqual(
            str(self.volunteer_user),
            u'volunteer@example.com',
        )
        self.assertEqual(
            str(self.organization_user),
            u'organization@example.com'
        )
        self.assertEqual(
            str(self.administrator_user),
            u'administrator@example.com'
        )

    def test__is_admin_or_volunteer(self):
        """Check if specified user has enabled/disabled administrator flag."""

        self.assertTrue(self.administrator_user.is_administrator)
        self.assertFalse(self.volunteer_user.is_administrator)
        self.assertFalse(self.organization_user.is_administrator)
