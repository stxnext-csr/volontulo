# -*- coding: utf-8 -*-

u"""
.. module:: test_userbadges
"""
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from volontulo.models import Badge
from volontulo.models import UserBadges
from volontulo.models import UserProfile


class TestUserBadgesModel(TestCase):
    u"""Tests for UserBadges model."""

    @classmethod
    def setUpTestData(cls):
        u"""Fixtures for all tests."""
        badge = Badge.objects.create(
            name=u'My Awesome Badge',
            slug=u'my-awesome-badge',
            priority=1,
        )
        userprofile = UserProfile.objects.create(
            user=User.objects.create_user(
                username=u'badgeduser@example.com',
                email=u'badgeduser@example.com',
                password=u'badgeduser'
            )
        )
        content_type = ContentType.objects.get(
            app_label='volontulo',
            model='offer',
        )

        UserBadges.objects.create(
            userprofile=userprofile,
            badge=badge,
            description=u'Description of rules for badge assignment.',
            content_type=content_type,
        )

    def test__string_representation(self):
        u"""Test User Badges string representation."""
        userbadge = UserBadges.objects.get(pk=1)

        self.assertEqual(
            userbadge.description,
            u'Description of rules for badge assignment.'
        )
