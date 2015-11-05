# -*- coding: utf-8 -*-

u"""
.. module:: test_contactform
"""
from django.core import mail
from django.test import Client
from django.test import TestCase

from apps.volontulo.tests.common import Common


class TestPages(TestCase):
    u"""Class responsible for testing contact forms."""

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
    def test__get_contact_with_administrator_form_by_anonymous(self):
        u"""Request contact with administrator form by anonymous user."""
        response = self.client.get('/contact', follow=True)

        self.assertRedirects(
            response,
            '/login?next=/contact',
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            ('http://testserver/login?next=/contact', 302),
        )

    # pylint: disable=invalid-name
    def test__get_contact_with_administrator_form_by_volunteer(self):
        u"""Request contact with administrator form by volunteer user."""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/contact')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, u'Formularz kontaktowy')
        # pylint: disable=no-member
        self.assertIn('contact_form', response.context)

    # pylint: disable=invalid-name
    def test__get_contact_with_administrator_form_by_organization(self):
        u"""Request contact with administrator form by organization user."""
        self.client.post('/login', {
            'email': u'organization1@example.com',
            'password': 'organization1',
        })
        response = self.client.get('/contact')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, u'Formularz kontaktowy')
        # pylint: disable=no-member
        self.assertIn('contact_form', response.context)

    # pylint: disable=invalid-name
    def test__post_contact_with_administrator_form_by_anonymous(self):
        u"""Post to contact with administrator form by anonymous user."""
        response = self.client.get('/contact', follow=True)

        self.assertRedirects(
            response,
            '/login?next=/contact',
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            ('http://testserver/login?next=/contact', 302),
        )

    # pylint: disable=invalid-name
    def test__post_contact_with_administrator_form_by_volunteer(self):
        u"""Post to contact with administrator form by volunteer user."""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        # send with incorrect params
        form_params = {
            'applicant': 1,
            'administrator': 1,
            'name': u'',
            'email': u'',
            'phone_no': u'',
            'message': u'',
        }
        response = self.client.post(
            '/contact',
            form_params,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, u'Formularz kontaktowy')
        # pylint: disable=no-member
        self.assertIn('contact_form', response.context)
        self.assertContains(response, u'Proszę poprawić błędy w formularzu:')
        self.assertEqual(len(mail.outbox), 0)

        # send with correct params
        form_params = {
            'applicant': 'VOLUNTEER',
            'administrator': 1,
            'name': u'Bull Pillman',
            'email': u'pull.billman@example.com',
            'phone_no': u'+48 123 123 123',
            'message': u"My crime is that of curiosity."
        }
        response = self.client.post(
            '/contact',
            form_params,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, u'Formularz kontaktowy')
        # pylint: disable=no-member
        self.assertIn('contact_form', response.context)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, u'Kontakt z administratorem')
        self.assertContains(response, u'Email został wysłany.')

    # pylint: disable=invalid-name
    def test__post_contact_with_administrator_form_by_organization(self):
        u"""Post to contact with administrator form by organization user."""
        self.client.post('/login', {
            'email': u'organization1@example.com',
            'password': 'organization1',
        })
        # incorrect params
        form_params = {
            'applicant': 1,
            'administrator': 1,
            'name': u'',
            'email': u'',
            'phone_no': u'',
            'message': u'',
        }
        response = self.client.post(
            '/contact',
            form_params,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, u'Formularz kontaktowy')
        # pylint: disable=no-member
        self.assertIn('contact_form', response.context)
        self.assertEqual(len(mail.outbox), 0)
        self.assertContains(response, u'Proszę poprawić błędy w formularzu:')

        # correct params
        form_params = {
            'applicant': 'ORGANIZATION',
            'administrator': 1,
            'name': u'Bull Pillman',
            'email': u'pull.billman@example.com',
            'phone_no': u'+48 123 123 123',
            'message': u"My crime is that of curiosity."
        }
        response = self.client.post(
            '/contact',
            form_params,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, u'Formularz kontaktowy')
        # pylint: disable=no-member
        self.assertIn('contact_form', response.context)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, u'Kontakt z administratorem')
        self.assertContains(response, u'Email został wysłany.')
