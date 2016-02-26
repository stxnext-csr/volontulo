# -*- coding: utf-8 -*-

u"""
.. module:: test_regulations
"""
from django.test import Client
from django.test import TestCase

from apps.volontulo.tests import common

class TestAboutus(TestCase):
    u"""Class responsible for testing regulations specific views."""

    # pylint: disable=invalid-name
    def test__regulations(self):
        u"""Test getting regulations page as anonymous."""
        response = self.client.get('/regulations', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'regulations.html')
