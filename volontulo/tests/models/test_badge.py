# -*- coding: utf-8 -*-

u"""
.. module:: test_badge
"""
from __future__ import unicode_literals

from django.test import TestCase

from volontulo.models import Badge


class TestBadge(TestCase):
    u"""Tests for Badge model."""

    def setUp(self):
        u"""Set up each test."""
        self.badge = Badge(
            name='My simple badge',
            slug='my-simple-badge',
            priority=1
        )

    # pylint: disable=invalid-name
    def test__badge_string_reprezentation(self):
        """Test string representation of Badge model."""
        self.assertEqual(
            str(self.badge),
            'My simple badge'
        )
