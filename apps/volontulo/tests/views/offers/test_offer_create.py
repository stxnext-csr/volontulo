# -*- coding: utf-8 -*-

"""
.. module:: test_offer_create
"""

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from apps.volontulo.models import Offer
from apps.volontulo.models import Organization
from apps.volontulo.models import UserProfile


class TestOffersCreate(TestCase):
    """Class responsible for testing offer's create page."""

    @classmethod
    def setUpTestData(cls):
        """Set up data for all tests."""
        cls.organization = Organization.objects.create(
            name='Organization Name',
            address='',
            description='',
        )
        cls.organization.save()
        organization_user = User.objects.create_user(
            'organization@example.com',
            'organization@example.com',
            '123org'
        )
        organization_user.save()
        cls.organization_profile = UserProfile(
            user=organization_user,
        )
        cls.organization_profile.save()
        # pylint: disable=no-member
        cls.organization_profile.organizations.add(cls.organization)

        no_org_user = User.objects.create_user(
            'no_organ@example.com',
            'no_organ@example.com',
            '123no_org'
        )
        UserProfile.objects.create(
            user=no_org_user,
        )

    def setUp(self):
        """Set up each test."""
        self.client = Client()

    def test_offers_create_get_method(self):
        """Test page for offer creation - tendering template with form."""
        self.client.post('/login', {
            'email': 'organization@example.com',
            'password': '123org',
        })
        response = self.client.get('/offers/create')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_form.html')

    # pylint: disable=invalid-name
    def test_offers_create_no_org_get_method(self):
        """Test page for offer creation - tendering template with form."""
        self.client.post('/login', {
            'email': 'no_organ@example.com',
            'password': '123no_org',
        })
        response = self.client.get('/offers/create', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Nie masz jeszcze żadnej założonej organizacji"
            " na volontuloapp.org."
        )
        self.assertTemplateUsed(response, 'offers/offers_list.html')

    def test_offers_create_invalid_form(self):
        """Test attempt of creation of new offer with invalid form."""
        self.client.post('/login', {
            'email': 'organization@example.com',
            'password': '123org',
        })
        response = self.client.post('/offers/create', {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_form.html')
        self.assertContains(
            response,
            'Formularz zawiera niepoprawnie wypełnione pola'
        )

    def test_create_offer_without_date(self):
        """Test for creating offer without date."""
        self.client.post('/login', {
            'email': 'organization@example.com',
            'password': '123org',
        })

        response = self.client.post('/offers/create', {
            'organization': self.organization.id,
            'description': 'desc',
            'requirements': 'required requirements',
            'time_commitment': 'required time_commitment',
            'benefits': 'required benefits',
            'location': 'required location',
            'title': 'volontulo offer',
            'time_period': 'required time_period',
            'started_at': '',
            'finished_at': '',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        offer = Offer.objects.get(description='desc')
        self.assertEqual(offer.action_status, 'ongoing')

    def test_offers_create_valid_form(self):
        """Test attempt of creation of new offer with valid form."""
        self.client.post('/login', {
            'email': 'organization@example.com',
            'password': '123org',
        })
        for i in range(1, 4):
            response = self.client.post('/offers/create', {
                'organization': self.organization.id,
                'description': str(i),
                'requirements': 'required requirements',
                'time_commitment': 'required time_commitment',
                'benefits': 'required benefits',
                'location': 'required location',
                'title': 'volontulo offer',
                'time_period': 'required time_period',
                'started_at': '2015-11-01 11:11:11',
                'finished_at': '2015-11-01 11:11:11',
            }, follow=True)
            offer = Offer.objects.get(description=str(i))
            self.assertRedirects(
                response,
                '/offers/volontulo-offer/{}'.format(offer.id),
                302,
                200,
            )
            self.assertEqual(
                offer.organization,
                self.organization_profile.organizations.all()[0],
            )
            self.assertEqual(offer.description, str(i))
            self.assertEqual(offer.requirements, 'required requirements')
            self.assertEqual(
                offer.time_commitment,
                'required time_commitment'
            )
            self.assertEqual(offer.benefits, 'required benefits')
            self.assertEqual(offer.location, 'required location')
            self.assertEqual(offer.title, 'volontulo offer')
            self.assertEqual(offer.time_period, 'required time_period')
