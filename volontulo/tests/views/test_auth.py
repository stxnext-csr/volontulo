# -*- coding: utf-8 -*-

u"""
.. module:: test_auth
"""

from django.contrib.auth.models import User
from django.test import Client
from django.test import TransactionTestCase


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
