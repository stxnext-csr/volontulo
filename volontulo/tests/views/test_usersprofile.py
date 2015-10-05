# -*- coding: utf-8 -*-

u"""
.. module:: test_users
"""
from django.test import Client
from django.test import TestCase

from volontulo.tests.common import Common
from volontulo.models import Offer


class TestUsersProfile(TestCase):
    u"""Class responsible for testing users profile view."""

    @classmethod
    def setUpTestData(cls):
        # volunteer user - totally useless
        Common.initialize_empty_volunteer()
        # organization user - no offers
        Common.initialize_empty_organization()
        # volunteer user - badges, offers, organizations
        Common.initialize_filled_volunteer_and_organization()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    # pylint: disable=invalid-name
    def test__logged_user_profile_anonymous(self):
        u"""Testing user profile page for anonymous"""
        response = self.client.get('/me', follow=True)

        self.assertRedirects(
            response,
            'http://testserver/login?next=/me',
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            ('http://testserver/login?next=/me', 302),
        )

    # pylint: disable=invalid-name
    def test__logged_user_profile(self):
        u"""Testing default views on user profile form"""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/me')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_profile.html')
        # check if contain image upload form (all users)
        # pylint: disable=no-member
        self.assertIn('image', response.context)
        self.assertContains(response, u'Wybierz grafikę')

    # pylint: disable=invalid-name
    def test__logged_user_profile_empty_volunteer(self):
        u"""Testing user profile page for volunteers"""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/me')

        self.assertContains(response, u'Jako wolontariusz chciałbym')
        # pylint: disable=no-member
        self.assertIn('badges', response.context)
        self.assertContains(response, u'Nie masz jeszcze żadnych odznak')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        self.assertContains(
            response,
            u'Nie wyraziłeś chęci udziału w żadnej z dostępnych ofert.'
        )

    # pylint: disable=invalid-name
    def test__logged_user_profile_filled_volunteer(self):
        u"""Testing user profile page for volunteers"""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/me')

        self.assertContains(response, u'Jako wolontariusz chciałbym')
        # pylint: disable=no-member
        self.assertIn('badges', response.context)
        self.assertContains(response, u'Nie masz jeszcze żadnych odznak')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        self.assertContains(
            response,
            u'Nie wyraziłeś chęci udziału w żadnej z dostępnych ofert.'
        )

    # pylint: disable=invalid-name
    def test__logged_user_profile_empty_organization(self):
        u"""Testing user profile page for empty organization"""
        self.client.post('/login', {
            'email': u'organization1@example.com',
            'password': 'organization1',
        })
        response = self.client.get('/me')

        self.assertContains(response, u'Jako organizacja chciałbym')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        self.assertContains(
            response,
            u'Ta organizacja nie ma jeszcze żadnych ofert.'
        )

    # pylint: disable=invalid-name
    def test__logged_user_profile_filled_organization(self):
        u"""Testing user profile page for filled organization"""
        self.client.post('/login', {
            'email': u'organization2@example.com',
            'password': 'organization2',
        })
        response = self.client.get('/me')

        self.assertContains(response, u'Jako organizacja chciałbym')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        self.assertEqual(
            4,
            Offer.objects.all().count()
        )
        self.assertNotContains(
            response,
            u'Ta organizacja nie ma jeszcze żadnych ofert.'
        )
