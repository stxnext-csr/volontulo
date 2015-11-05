# -*- coding: utf-8 -*-

u"""
.. module:: test_auth
"""
from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.test import TransactionTestCase

from apps.volontulo.tests.common import Common


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
        self.assertContains(
            response,
            u'Na podany przy rejestracji email został wysłany link '
            u'aktywacyjny. Aby w pełni wykorzystać konto należy je aktywować '
            u'poprzez kliknięcie linku lub wklejenie go w przeglądarce.'
        )

        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(User.objects.all().count(), 1)

    # pylint: disable=invalid-name
    def test__register_authenticated_user(self):
        u"""Check if authenticated user can access register page."""
        # volunteer user
        Common.initialize_empty_volunteer()

        self.client.post('/login', {
            'email': 'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/login', follow=True)

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
        self.assertIn('_auth_user_id', self.client.session)
        self.assertContains(
            response,
            u'Jesteś już zalogowany.'
        )


class TestLogin(TestCase):
    u"""Class responsible for testing user login view."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up fixtures data for test."""
        # volunteer user
        Common.initialize_empty_volunteer()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    def test__get_login_by_anonymous(self):
        u"""Get login form by anonymous user"""
        response = self.client.get('/login')

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        self.assertContains(response, u'Logowanie')
        self.assertContains(
            response,
            u'Nie pamiętasz hasła? Możemy pomóc!'
        )
        self.assertContains(
            response,
            u'Email address:'
        )
        self.assertContains(
            response,
            u'Password:'
        )

    def test__get_login_by_authorized(self):
        u"""Get login form by authorized user"""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/login', follow=True)

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
        self.assertIn('_auth_user_id', self.client.session)

    # pylint: disable=invalid-name
    def test__post_login_by_anonymous_user(self):
        u"""Post to login form by anonymous"""
        # incorrect email or password
        form_params = {
            'email': 'whoami@example.com',
            'password': 'volunteer1',
        }
        response = self.client.post(
            '/login',
            form_params,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u"Nieprawidłowy email lub hasło!")
        form_params = {
            'email': 'volunteer1@example.com',
            'password': 'xxx',
        }
        response = self.client.post(
            '/login',
            form_params,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u"Nieprawidłowy email lub hasło!")

        # email and password is correct but and user is not active
        user = User.objects.get(id=1)
        user.is_active = False
        user.save()

        form_params = {
            'email': 'volunteer1@example.com',
            'password': 'volunteer1',
        }
        response = self.client.post(
            '/login',
            form_params,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u"Konto jest nieaktywne, skontaktuj się z administratorem.")
        self.assertNotIn('_auth_user_id', self.client.session)

        # email and password is correct and user is active
        user.is_active = True
        user.save()
        form_params = {
            'email': 'volunteer1@example.com',
            'password': 'volunteer1',
        }
        response = self.client.post(
            '/login',
            form_params,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u"Poprawnie zalogowano")
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

    # pylint: disable=invalid-name
    def test__post_login_by_authorized_user(self):
        u"""Post to login form by authorized"""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/login', follow=True)

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


class TestLogout(TestCase):
    u"""Class responsible for testing user logout view."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up fixtures data for test."""
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
        u"""Testing logout view for authenticated user."""
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

    def test__login_authenticated_user(self):
        u"""Check if authenticated user can access login page."""
        self.client.post('/login', {
            'email': 'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/login', follow=True)

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
        self.assertIn('_auth_user_id', self.client.session)
        self.assertContains(
            response,
            u'Jesteś już zalogowany.'
        )
