# -*- coding: utf-8 -*-

u"""
.. module:: test_newsletter
"""
from django.test import TestCase


class TestAboutus(TestCase):
    u"""Class responsible for testing newsletter specific views."""

    # pylint: disable=invalid-name
    def test__newsletter(self):
        u"""Test getting newsletter signup page as anonymous."""
        response = self.client.get('/newsletter', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsletter_signup.html')
