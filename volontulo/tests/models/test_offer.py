# -*- coding: utf-8 -*-

u"""
.. module:: test_offer
"""
from django.contrib.auth.models import User
from django.test import TestCase

from volontulo.models import Offer
from volontulo.models import Organization


class TestOfferModel(TestCase):
    u"""Tests for Offer model."""

    @classmethod
    def setUpTestData(cls):
        u"""Fixtures for Offer model unittests."""
        volunteers = [
            User.objects.create(
                username=u'volunteer1@example.com',
                email=u'volunteer1@example.com',
                password=u'volunteer1'
            ),
            User.objects.create(
                username=u'volunteer2@example.com',
                email=u'volunteer2@example.com',
                password=u'volunteer2'
            ),
            User.objects.create(
                username=u'volunteer3@example.com',
                email=u'volunteer3@example.com',
                password=u'volunteer3'
            ),
        ]
        offer = Offer.objects.create(
            organization=Organization.objects.create(
                name=u'Some great organization',
                address=u'Our great organization address,',
                description=u'Great description of great organization'
            ),
            description=u'A lot of unnecessary work.',
            requirements=u'Patience, lot of free time',
            time_commitment='12.12.2015',
            benefits=u'Friends with benefits',
            location=u'Poland, Poznań',
            title=u'This is example offer title',
            time_period=u'2-5 times a week',
            started_at='2015-10-12 10:11:12',
            finished_at='2015-12-12 11:12:13',
        )
        for volunteer in volunteers:
            offer.volunteers.add(volunteer)

    def test__string_representation(self):
        u"""Test Offer model string reprezentation."""
        offer = Offer.objects.get(id=1)

        self.assertEqual(offer.title, u'This is example offer title')
        self.assertEqual(offer.volunteers.count(), 3)
        self.assertEqual(
            offer.volunteers.all()[0].email,
            u'volunteer1@example.com'
        )
        self.assertEqual(
            offer.volunteers.all()[1].email,
            u'volunteer2@example.com'
        )
        self.assertEqual(
            offer.volunteers.all()[2].email,
            u'volunteer3@example.com'
        )
        self.assertEqual(offer.organization.name, u'Some great organization')
        self.assertEqual(offer.description, u'A lot of unnecessary work.')
        self.assertEqual(offer.requirements, u'Patience, lot of free time')
        self.assertEqual(offer.time_commitment, '12.12.2015')
        self.assertEqual(offer.benefits, u'Friends with benefits')
        self.assertEqual(offer.location, u'Poland, Poznań')
        self.assertEqual(offer.time_period, u'2-5 times a week')


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
            status_old='ACTIVE',
            started_at='2015-10-12 10:11:12',
            finished_at='2015-12-12 11:12:13',
            offer_status='published',
            recruitment_status='open',
            action_status='ongoing',
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

    def test__offer_time_commit_field(self):
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
            self.offer.status_old,
            'ACTIVE'
        )
