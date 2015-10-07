# -*- coding: utf-8 -*-

u"""
.. module:: test_auth
"""
from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.test import TransactionTestCase

from volontulo.tests.common import Common


class TestRegister(TransactionTestCase):
    u"""Tests for register view."""

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    def test_get_method(self):
        u"""Test for get method for view."""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_invalid_form(self):
        u"""Test for post method with invalid form."""
        response = self.client.post('/register', {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')
        self.assertContains(
            response,
            u'Wprowadzono nieprawidłowy email lub hasło',
        )
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_user_already_exists(self):
        u"""Test for attempt of registration for user, that already exists."""
        User.objects.create_user(
            u'existing@example.com',
            u'existing@example.com',
            u'123existing'
        )
        response = self.client.post('/register', {
            'email': u'existing@example.com',
            'password': u'123existing',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')
        self.assertContains(
            response,
            u'Użytkownik o podanym emailu już istnieje',
        )
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(User.objects.all().count(), 1)

    def test_successful_registration(self):
        u"""Test for attempt of registration for new user."""
        response = self.client.post('/register', {
            'email': u'new@example.com',
            'password': u'123new',
        }, follow=True)
        self.assertRedirects(response, '/', 302, 200)
        self.assertContains(
            response,
            u'Rejestracja przebiegła pomyślnie',
        )
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(User.objects.all().count(), 1)


class TestAuth(TestCase):
    u"""Class responsible for testing users authentication view."""

    @classmethod
    def setUpTestData(cls):
        # volunteer user
        Common.initialize_empty_volunteer()

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
        self.assertNotIn('_auth_user_id', self.client.session)

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
        self.assertNotIn('_auth_user_id', self.client.session)
