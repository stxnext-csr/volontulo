# -*- coding: utf-8 -*-

u"""
.. module:: test_organizations
"""
from django.core import mail
from django.test import Client
from django.test import TestCase

from volontulo.models import Organization
from volontulo.tests.common import Common


class TestOrganizations(TestCase):
    u"""Class responsible for testing organization specific views."""

    @classmethod
    def setUpTestData(cls):
        u"""Data fixtures for all tests."""
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
    def test__organization_list(self):
        u"""Test getting organization list as anonymous."""
        response = self.client.get('/organizations', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organizations/list.html')
        # pylint: disable=no-member
        self.assertIn('organizations', response.context)
        self.assertEqual(Organization.objects.all().count(), 2)

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

    def test__get_empty_organization_view_by_anonymous(self):
        u"""Request for empty organization view by anonymous user."""
        response = self.client.get('/organizations/organization-1/1')

        self.assertEqual(response.status_code, 200)
        # pylint: disable=no-member
        self.assertIn('contact_form', response.context)
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        # pylint: disable=no-member
        self.assertIn('organization', response.context)
        self.assertContains(response, u'Nazwa')
        self.assertContains(response, u'Opis')
        self.assertContains(response, u'Adres')
        self.assertContains(response, u'Formularz kontaktowy')
        self.assertContains(
            response,
            u'Ta organizacja nie ma jeszcze żadnych ofert.'
        )
        self.assertTemplateUsed(
            response,
            'organizations/organization_view.html'
        )
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, u'Wyślij')

    def test__get_filled_organization_view_by_anonymous(self):
        u"""Request for filled organization view by anonymous user."""
        response = self.client.get('/organizations/organization-2/2')

        self.assertNotContains(
            response,
            u'Ta organizacja nie ma jeszcze żadnych ofert.'
        )
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        self.assertEqual(len(response.context['offers']), 14)

    def test__get_empty_organization_view_by_volunteer(self):
        u"""Requesting for empty organization view by volunteer user."""
        self.client.post('/login', {
            'email': u'volunteer2@example.com',
            'password': 'volunteer2',
        })
        response = self.client.get('/organizations/organization-1/1')

        self.assertContains(response, u'Organization 1')
        # pylint: disable=no-member
        self.assertIn('allow_edit', response.context)
        self.assertFalse(response.context['allow_edit'])
        self.assertNotContains(response, u'Edytuj organizację')
        # pylint: disable=no-member
        self.assertIn('allow_offer_create', response.context)
        self.assertFalse(response.context['allow_offer_create'])
        self.assertNotContains(response, u'Dodaj ofertę')

    def test__get_empty_organization_view_by_organization(self):
        u"""Request for empty organization view by organization user."""
        self.client.post('/login', {
            'email': u'organization1@example.com',
            'password': 'organization1',
        })
        response = self.client.get(
            '/organizations/organization-1/1',
            follow=True
        )
        # pylint: disable=no-member
        self.assertIn('allow_contact', response.context)
        self.assertIn('allow_edit', response.context)
        self.assertIn('allow_offer_create', response.context)
        self.assertFalse(response.context['allow_contact'])
        self.assertTrue(response.context['allow_edit'])
        self.assertTrue(response.context['allow_offer_create'])
        self.assertContains(response, u'Edytuj organizację')
        self.assertContains(response, u'Dodaj ofertę')

        self.client.get('/logout')
        self.client.post('/login', {
            'email': u'organization2@example.com',
            'password': 'organization2',
        })
        response = self.client.get(
            '/organizations/organization-1/1',
            follow=True
        )
        self.assertNotContains(response, u'Edytuj organizację')
        self.assertNotContains(response, u'Dodaj ofertę')
        self.assertIn('allow_contact', response.context)
        self.assertTrue(response.context['allow_contact'])
        self.assertFalse(response.context['allow_edit'])
        self.assertFalse(response.context['allow_offer_create'])

    def test__get_filled_organization_view_by_organization(self):
        u"""Request for filled organization view by organization user."""
        self.client.post('/login', {
            'email': u'organization2@example.com',
            'password': 'organization2',
        })
        response = self.client.get(
            '/organizations/organization-2/2',
            follow=True
        )
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        self.assertEqual(len(response.context['offers']), 14)

    def test__post_contact_form_on_organization_view_by_anonymous(self):
        u"""Post contact form to organization view by anonymous user."""
        form_params = {
            'name': u'',
            'email': u'',
            'phone_no': u'',
            'message': u'',
        }
        response = self.client.post(
            '/organizations/organization-1/1',
            form_params,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u"Formularz zawiera nieprawidłowe dane")

        form_params = {
            'name': u'Mister Volunteer',
            'email': u'mister.volunteer@example.com',
            'phone_no': u'+48 123 123 123',
            'message': u'',
        }
        response = self.client.post(
            '/organizations/organization-1/1',
            form_params,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u'Formularz zawiera nieprawidłowe dane')
        self.assertContains(response, u'Mister Volunteer')
        self.assertContains(response, u'+48 123 123 123')
        self.assertContains(response, u'mister.volunteer@example.com')

        form_params = {
            'name': u'',
            'email': u'',
            'phone_no': u'',
            'message': u'Wiadomość dla organizacji',
        }
        response = self.client.post(
            '/organizations/organization-1/1',
            form_params,
            follow=True
        )
        self.assertContains(response, u'Wiadomość dla organizacji')
        self.assertEqual(len(mail.outbox), 0)

    def test__post_contact_form_on_organization_view_by_volunteer(self):
        u"""Post contact form to organization view by volunteer user."""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        form_params = {
            'name': u'',
            'email': u'',
            'phone_no': u'',
            'message': u'',
            'organization': 1,
        }
        response = self.client.post(
            '/organizations/organization-2/2',
            form_params,
            follow=True
        )
        self.assertContains(response, u'Formularz zawiera nieprawidłowe dane')

        form_params = {
            'name': u'Mister volunteer',
            'email': u'mister.volunteer@example.com',
            'phone_no': u'+48 123 123 123',
            'message': u'To jest wiadomość dla organizacji od wolontariusza',
            'organization': 1,
        }
        response = self.client.post(
            '/organizations/organization-2/2',
            form_params
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, u'Kontakt od wolontariusza')
        self.assertContains(
            response,
            u'Email został wysłany.'
        )

    def test__post_contact_form_on_organization_view_by_organization(self):
        u"""Post contact form to organization view by organization user."""
        self.client.post('/login', {
            'email': u'organization2@example.com',
            'password': 'organization2',
        })
        form_params = {
            'name': u'Mister volunteer',
            'email': u'mister.volunteer@example.com',
            'phone_no': u'+48 123 123 123',
            'message': u'To jest wiadomość dla organizacji od wolontariusza',
            'organization': 1,
        }
        response = self.client.post(
            '/organizations/organization-1/1',
            form_params,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, u'Kontakt od wolontariusza')
        self.assertContains(
            response,
            u'Email został wysłany.'
        )
