# -*- coding: utf-8 -*-

u"""
.. module:: test_pages
"""
from django.test import Client
from django.test import TestCase


class TestPages(TestCase):
    u"""Class responsible for testing various pages."""

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

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
