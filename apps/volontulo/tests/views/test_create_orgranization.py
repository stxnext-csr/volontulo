# -*- coding: utf-8 -*-

u"""
.. module:: test_create_organization
"""
from volontulo.tests.views.test_organizations import TestOrganizations

from volontulo.models import Organization


class TestCreateOrganization(TestOrganizations):
    u"""Class responsible for testing editing organization specific views."""

    # pylint: disable=invalid-name
    def test__create_organization_get_form_anonymous(self):
        u"""Test getting form for creating organization as anonymous."""
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
    def test__create_organization_get_form_authorized(self):
        u"""Test getting form for creating organization as authorized."""
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
    def test__create_organization_post_form_anonymous(self):
        u"""Test posting form for creating organization as anonymous."""
        # Disable for anonymous user
        response = self.client.post('/organizations/create')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            'http://testserver/login?next=/organizations/create',
            302,
            200,
        )

    # pylint: disable=invalid-name
    def test__create_empty_organization_post_form(self):
        u"""Test posting form for creating empty (not filled) organization."""
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

    # pylint: disable=invalid-name
    def test__create_organization_post_form_fill_fields(self):
        u"""Test posting form and check fields population."""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        form_params = {
            'name': u'Halperin Organix',
            'address': u'East Street 123',
        }
        response = self.client.post('/organizations/create', form_params)

        # pylint: disable=no-member
        self.assertIn('organization', response.context)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            u'Halperin Organix'
        )
        self.assertContains(
            response,
            u'East Street 123'
        )

        form_params = {
            'description': u'User unfriendly organization',
        }
        response = self.client.post('/organizations/create', form_params)
        self.assertIn('organization', response.context)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            u'User unfriendly organization'
        )

    def test__create_valid_organization_form_post(self):
        u"""Test posting valid form for creating organization."""
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
            '/organizations/halperin-organix/3',
            302,
            200,
        )
        self.assertContains(
            response,
            u"Organizacja została dodana."
        )
        record = Organization.objects.get(id=3)
        self.assertEqual(record.id, 3)
        self.assertEqual(record.name, u'Halperin Organix')
        self.assertEqual(record.address, u'East Street 123')
        self.assertEqual(record.description, u'User unfriendly organization')
