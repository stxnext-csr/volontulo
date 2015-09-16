# -*- coding: utf-8 -*-
u"""
.. module:: tests
"""

from django.test import TestCase
from volontulo.models import Offer
from volontulo.models import Organization


class OfferTestCase(TestCase):
    u"""Tests for Offer model."""

    def setUp(self):
        self.organization = Organization.objects.create(
            name=u"Halperin Organix"
        )
        self.offer = Offer.objects.create(
            organization=self.organization,
            description=u"Dokładny opis oferty",
            requirements=u"Dokładny opis wymagań",
            time_commitment=u"333 dni w roku",
            benefits=u"Wszelkie korzyści z uczestnictwa w wolontariacie",
            location=u"Polska, Poznań",
            title=u"Zwięzły tytuł oferty",
            time_period=u"Od 23.09.2015 do 25.12.2016",
            status='ACTIVE'
        )

    def test__organization_name(self):
        u"""Testing organization name field"""
        self.assertEqual(self.organization.name, u"Halperin Organix")

    def test__offer_organization_field(self):
        u"""Testing organization name as oneToOne relation"""
        self.assertIsInstance(self.offer.organization, Organization)
        self.assertEqual(self.offer.organization.name, u"Halperin Organix")

    def test__offer_description_field(self):
        u"""Testing offer description field"""
        self.assertEqual(self.offer.description, u"Dokładny opis oferty")

    def test__offer_requiremends_field(self):
        u"""Testing offer requirements field"""
        self.assertEqual(self.offer.requirements, u"Dokładny opis wymagań")

    def test__offer_time_commitment_field(self):  # pylint: disable=invalid-name
        u"""Testing offer time commitment field"""
        self.assertEqual(self.offer.time_commitment, u"333 dni w roku")

    def test__offer_benefits_field(self):
        u"""Testing offer benefits field"""
        self.assertEqual(
            self.offer.benefits,
            u"Wszelkie korzyści z uczestnictwa w wolontariacie"
        )

    def test__offer_location_field(self):
        u"""Testing offer location field"""
        self.assertEqual(
            self.offer.location,
            u"Polska, Poznań"
        )

    def test__offer_title_field(self):
        u"""Testing offer title field"""
        self.assertEqual(
            self.offer.title,
            u"Zwięzły tytuł oferty"
        )

    def test__offer_time_period_field(self):
        u"""Testing offer time_period field"""
        self.assertEqual(
            self.offer.time_period,
            u"Od 23.09.2015 do 25.12.2016",
        )

    def test__offer_status_field(self):
        u"""Testing offer status field"""
        self.assertEqual(
            self.offer.status,
            'ACTIVE'
        )
