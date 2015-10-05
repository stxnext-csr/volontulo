# -*- coding: utf-8 -*-

u"""
.. module:: test_auth
"""
from django.test import Client
from django.test import TestCase

from volontulo.tests.views.test_usersprofile import TestUsersProfile


class TestAuth(TestCase):
    u"""Class responsible for testing users authentication view."""

    @classmethod
    def setUpTestData(cls):
        # volunteer user
        TestUsersProfile.initialize_empty_volunteer()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    # pylint: disable=invalid-name
    def test__logged_out_anonymous_user(self):
        u"""Testing logout view for anonymous user"""
        response = self.client.get('/logout', follow=True)

        self.assertRedirects(
            response,
            'http://testserver/login?next=/logout',
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            ('http://testserver/login?next=/logout', 302),
        )

    def test__logged_out_authenticated_user(self):
        u"""Testing logout view for authenticated user"""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/logout', follow=True)

        self.assertRedirects(
            response,
            '/',
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            ('http://testserver/', 302),
        )
        self.assertContains(
            response,
            u"Użytkownik został wylogowany!"
        )
