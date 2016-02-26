# -*- coding: utf-8 -*-

u"""
.. module:: test_pages
"""
from django.test import Client
from django.test import TestCase

from apps.volontulo.tests import common


class TestPages(TestCase):
    u"""Class responsible for testing various pages."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        common.initialize_filled_volunteer_and_organization()
        common.initialize_administrator()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    def test__homepage_for_anonymous(self):
        u"""Home page for anonymous users."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        # pylint: disable=no-member
        self.assertEqual(len(response.context['offers']), 4)

    # pylint: disable=invalid-name
    def test__homepage_for_volunteer_and_organization(self):
        u"""Home page for volunteers and organizations.

        There's currently no difference for anonymous
        or volunteer/organization - for now.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        # pylint: disable=no-member
        self.assertEqual(len(response.context['offers']), 4)

    # pylint: disable=invalid-name
    def test__homepage_for_administrator(self):
        u"""Home page for administrators."""
        self.client.post('/login', {
            'email': u'admin_user@example.com',
            'password': 'admin_password',
        })
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/list_offers.html')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        # pylint: disable=no-member
        self.assertEqual(len(response.context['offers']), 10)

        offers = {u'NEW': 0, u'ACTIVE': 0, u'SUSPENDED': 0}
        for offer in response.context['offers']:
            offers[offer.status_old] += 1

        self.assertEqual(offers[u'ACTIVE'], 0)
        self.assertEqual(offers[u'NEW'], 5)
        self.assertEqual(offers[u'SUSPENDED'], 5)

    def test__get_site_news_staticpage(self):
        u"""Site news static page"""
        response = self.client.get('/pages/site-news')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/site-news.html')
        self.assertContains(response, u'Informacje o działaniu portalu')

    # pylint: disable=invalid-name
    def test__get_organization_faq_staticpage(self):
        u"""Organization FAQ static page"""
        response = self.client.get('/pages/faq-organizations')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/faq-organizations.html')
        self.assertContains(response, u'Często zadawane pytania')

    # pylint: disable=invalid-name
    def test__get_volunteer_faq_staticpage(self):
        u"""Volunteer FAQ static page"""
        response = self.client.get('/pages/faq-volunteers')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/faq-volunteers.html')
        self.assertContains(response, u'Często zadawane pytania')

    # pylint: disable=invalid-name
    def test__get_regulations_staticpage(self):
        u"""Regulations FAQ static page"""
        response = self.client.get('/pages/regulations')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/regulations.html')
        self.assertContains(response, u'Regulamin')

    def test_office_subpage(self):
        u"""Test office subpage."""
        response = self.client.get('/office')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/office.html')
        self.assertContains(response,
                            u'Dyżury dla wolontariuszy oraz organizacji')
