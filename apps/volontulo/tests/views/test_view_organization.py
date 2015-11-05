# -*- coding: utf-8 -*-

u"""
.. module:: test_view_organization
"""
from django.core import mail

from apps.volontulo.tests.views.test_organizations import TestOrganizations


class TestCreateOrganization(TestOrganizations):
    u"""Class responsible for testing editing organization specific views."""

    # pylint: disable=invalid-name
    def test__get_empty_organization_view_by_anonymous(self):
        u"""Request for empty organization view by anonymous user."""
        response = self.client.get('/organizations/organization-1/{}'.format(
            self.organization.id
        ))

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
            u'Ta organizacja nie utworzyła jeszcze żadnych ofert.'
        )
        self.assertTemplateUsed(
            response,
            'organizations/organization_view.html'
        )
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, u'Wyślij')

    # pylint: disable=invalid-name
    def test__get_filled_organization_view_by_anonymous(self):
        u"""Request for filled organization view by anonymous user."""
        response = self.client.get('/organizations/organization-2/{}'.format(
            self.organization2.id
        ))

        self.assertNotContains(
            response,
            u'Ta organizacja nie utworzyła jeszcze żadnych ofert.'
        )
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        self.assertEqual(len(response.context['offers']), 14)

    # pylint: disable=invalid-name
    def test__get_empty_organization_view_by_volunteer(self):
        u"""Requesting for empty organization view by volunteer user."""
        self.client.post('/login', {
            'email': u'volunteer2@example.com',
            'password': 'volunteer2',
        })
        response = self.client.get('/organizations/organization-1/{}'.format(
            self.organization.id
        ))

        self.assertContains(response, u'Organization 1')
        # pylint: disable=no-member
        self.assertIn('allow_edit', response.context)
        self.assertFalse(response.context['allow_edit'])
        self.assertNotContains(response, u'Edytuj organizację')
        # pylint: disable=no-member
        self.assertIn('allow_offer_create', response.context)
        self.assertFalse(response.context['allow_offer_create'])
        self.assertNotContains(response, u'Dodaj ofertę')

    # pylint: disable=invalid-name
    def test__get_empty_organization_view_by_organization(self):
        u"""Request for empty organization view by organization user."""
        self.client.post('/login', {
            'email': u'organization1@example.com',
            'password': 'organization1',
        })
        response = self.client.get(
            '/organizations/organization-1/{}'.format(self.organization.id),
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
            '/organizations/organization-1/{}'.format(self.organization.id),
            follow=True
        )
        self.assertNotContains(response, u'Edytuj organizację')
        self.assertNotContains(response, u'Dodaj ofertę')
        self.assertIn('allow_contact', response.context)
        self.assertTrue(response.context['allow_contact'])
        self.assertFalse(response.context['allow_edit'])
        self.assertFalse(response.context['allow_offer_create'])

    # pylint: disable=invalid-name
    def test__get_filled_organization_view_by_organization(self):
        u"""Request for filled organization view by organization user."""
        self.client.post('/login', {
            'email': u'organization2@example.com',
            'password': 'organization2',
        })
        response = self.client.get(
            '/organizations/organization-2/{}'.format(self.organization2.id),
            follow=True
        )
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        self.assertEqual(len(response.context['offers']), 14)

    # pylint: disable=invalid-name
    def test__post_contact_form_on_organization_view_by_anonymous(self):
        u"""Post contact form to organization view by anonymous user."""
        form_params = {
            'name': u'',
            'email': u'',
            'phone_no': u'',
            'message': u'',
        }
        response = self.client.post(
            '/organizations/organization-1/{}'.format(self.organization.id),
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
            '/organizations/organization-1/{}'.format(self.organization.id),
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
            '/organizations/organization-1/{}'.format(self.organization.id),
            form_params,
            follow=True
        )
        self.assertContains(response, u'Wiadomość dla organizacji')
        self.assertEqual(len(mail.outbox), 0)

    # pylint: disable=invalid-name
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
            '/organizations/organization-2/{}'.format(self.organization2.id),
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
            '/organizations/organization-2/{}'.format(self.organization2.id),
            form_params
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, u'Kontakt od wolontariusza')
        self.assertContains(
            response,
            u'Email został wysłany.'
        )

    # pylint: disable=invalid-name
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
            '/organizations/organization-1/{}'.format(self.organization.id),
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
