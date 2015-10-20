# -*- coding: utf-8 -*-

u"""
.. module:: test_organization
"""
from __future__ import unicode_literals
from django.test import TestCase

from volontulo.models import Organization


class TestOrganization(TestCase):
    """Class responsible for testing organization model."""

    def setUp(self):
        """Set up each test."""
        self.organization = Organization.objects.create(
            name="Sample organization",
            address="Sample organization address",
            description="Sample organization description",
        )

    def test__string_reprezentation(self):
        """String reprezentation of an organization object."""
        self.assertEqual(
            str(self.organization),
            "Sample organization"
        )
