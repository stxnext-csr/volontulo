# -*- coding: utf-8 -*-

u"""
.. module:: test_users
"""
from django.test import Client
from django.test import TestCase

from apps.volontulo.tests import common
from apps.volontulo.models import Offer


class TestUsersProfile(TestCase):
    u"""Class responsible for testing users profile view."""

    @classmethod
    def setUpTestData(cls):
        # volunteer user - totally useless
        common.initialize_empty_volunteer()
        # organization user - no offers
        common.initialize_empty_organization()
        # volunteer user - offers, organizations
        common.initialize_filled_volunteer_and_organization()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    def test__logged_user_profile_anonymous(self):
        u"""Testing user profile page for anonymous."""
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

    def test__logged_user_profile(self):
        u"""Testing default views on user profile form."""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/me')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_profile.html')
        # check if contain image upload form (all users)
        self.assertIn('image', response.context)
        self.assertContains(response, u'Wybierz grafikę')

    def test__logged_user_profile_empty_volunteer(self):
        u"""Testing user profile page for volunteers."""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/me')

        self.assertIn('offers', response.context)
        self.assertContains(
            response,
            u"Zgłoś się w jednej z dostępnych "
            u"ofert wolontariuatu i zapełnij to miejsce."
        )

    def test__logged_user_profile_filled_volunteer(self):
        u"""Testing user profile page for volunteers."""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/me')

        self.assertIn('offers', response.context)
        self.assertContains(
            response,
            u"Zgłoś się w jednej z dostępnych "
            u"ofert wolontariuatu i zapełnij to miejsce."
        )

    def test__logged_user_profile_empty_organization(self):
        u"""Testing user profile page for empty organization."""
        self.client.post('/login', {
            'email': u'organization1@example.com',
            'password': 'organization1',
        })
        response = self.client.get('/me')

        self.assertIn('offers', response.context)
        self.assertContains(
            response,
            u'Ta organizacja nie utworzyła jeszcze żadnych ofert.'
        )

    def test__logged_user_profile_filled_organization(self):
        u"""Testing user profile page for filled organization."""
        self.client.post('/login', {
            'email': u'organization2@example.com',
            'password': 'organization2',
        })
        response = self.client.get('/me')

        self.assertIn('offers', response.context)
        self.assertEqual(
            4,
            Offer.objects.all().filter(status_old=u'ACTIVE').count()
        )
        self.assertNotContains(
            response,
            u'Ta organizacja nie utworzyła jeszcze żadnych ofert.'
        )

    def test__userprofile_phone_no(self):
        u"""Testing user profile page for filled organization."""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/me')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_profile.html')
        self.assertIn('profile_form', response.context)
        self.assertContains(response, u'333666999')

    def test__userprofile_first_and_last_name(self):
        """Testing user profile page for filled first and last name."""
        self.client.post('/login', {
            'email': 'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/me')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_profile.html')
        self.assertIn('profile_form', response.context)
        self.assertContains(response, 'Grzegorz')
        self.assertContains(response, 'Brzęczyszczykiewicz')

    def test__no_email_field_on_edit_profile_form(self):
        """Test if Email field is not visible edit profile form."""

        self.client.post('/login', {
            'email': 'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/me')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_profile.html')
        self.assertIn('profile_form', response.context)
        self.assertNotContains(response, 'Email')
