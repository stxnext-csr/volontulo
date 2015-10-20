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
