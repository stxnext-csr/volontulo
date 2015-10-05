# -*- coding: utf-8 -*-

u"""
.. module:: test_organizations
"""
from django.test import Client
from django.test import TestCase

from volontulo.models import Organization
from volontulo.tests.views.test_usersprofile import TestUsersProfile


class TestOrganizations(TestCase):
    u"""Class responsible for testing organization specific views."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        # volunteer user - totally useless
        TestUsersProfile.initialize_empty_volunteer()
        # organization user - no offers
        TestUsersProfile.initialize_empty_organization()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    # pylint: disable=invalid-name
    def test__create_organization_get_form_anonymous_user(self):
        u"""Test getting form for creating organization as anonymous"""
        # Disable for anonymous user
        response = self.client.get('/organizations/create')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            'http://testserver/login?next=/organizations/create',
            302,
            200,
        )

    # pylint: disable=invalid-name
    def test__create_organization_get_form_authorized_user(self):
        u"""Test getting form for creating organization as authorized"""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/organizations/create')

        self.assertTemplateUsed(
            response,
            'organizations/organization_form.html'
        )
        # pylint: disable=no-member
        self.assertIn('organization', response.context)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u'Tworzenie organizacji')

    # pylint: disable=invalid-name
    def test__create_organization_post_form_anonymous_user(self):
        u"""Test posting form for creating organization as anonymous"""
        # Disable for anonymous user
        response = self.client.get('/organizations/create')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            'http://testserver/login?next=/organizations/create',
            302,
            200,
        )

    # pylint: disable=invalid-name
    def test__create_empty_organization_post_form(self):
        u"""Test posting form for creating organization as anonymous"""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        form_params = {
            'name': u'',
            'address': u'',
            'description': u'',
        }
        response = self.client.post('/organizations/create', form_params)

        # pylint: disable=no-member
        self.assertIn('organization', response.context)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            u"Należy wypełnić wszystkie pola formularza."
        )

    def test__create_valid_organization_form_post(self):
        u"""Test posting valid form for creating organization"""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        form_params = {
            'name': u'Halperin Organix',
            'address': u'East Street 123',
            'description': u'User unfriendly organization',
        }
        response = self.client.post(
            '/organizations/create',
            form_params,
            follow=True
        )

        self.assertRedirects(
            response,
            '/organizations/halperin-organix/2',
            302,
            200,
        )
        self.assertContains(
            response,
            u"Organizacja została dodana."
        )
        record = Organization.objects.get(id=2)
        self.assertEqual(record.id, 2)
