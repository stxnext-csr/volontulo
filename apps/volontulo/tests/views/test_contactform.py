# -*- coding: utf-8 -*-

u"""
.. module:: test_contactform
"""
from django.core import mail
from django.test import Client
from django.test import TestCase

from apps.volontulo.tests import common


class TestPages(TestCase):
    u"""Class responsible for testing contact forms."""

    test_admin_email = test_admin_username = 'admin@admin.com'
    test_admin_password = 'admin_password'

    @classmethod
    def setUpTestData(cls):
        # admin user
        cls.admin = common.initialize_administrator(
            username=cls.test_admin_username, email=cls.test_admin_email,
            password=cls.test_admin_password
        )
        # volunteer user - totally useless
        cls.volunteer = common.initialize_empty_volunteer()
        # organization user - no offers
        common.initialize_empty_organization()
        # volunteer user - offers, organizations
        common.initialize_filled_volunteer_and_organization()

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
    def test__contact_with_admin_form_by_volunteer_val_error(self):
        u"""Post to contact with administrator form by volunteer user
        assuming validation error."""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })

        form_params = {
            'applicant': 'VOLUNTEER',
            'administrator': self.admin.id,
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

    def test__contact_with_admin_form_by_volunteer(self):
        u"""Post to contact with administrator form by volunteer user"""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        form_params = {
            'applicant': 'VOLUNTEER',
            'administrator': self.admin.id,
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
    def test__contact_with_admin_form_by_organization_val_error(self):
        u"""
        Post to contact with administrator form by organization user
        validation error.
        """
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

    def test__contact_with_admin_form_by_organization_val_success(self):
        u"""
        Post to contact with administrator form by organization user
        validation success.
        """
        self.client.post('/login', {
            'email': self.admin.email,
            'password': self.test_admin_password
        })

        # correct params
        form_params = {
            'applicant': 'ORGANIZATION',
            'administrator': self.admin.id,
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
