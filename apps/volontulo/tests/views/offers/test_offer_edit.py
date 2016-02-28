# -*- coding: utf-8 -*-

"""
.. module:: test_offer_edit
"""

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from apps.volontulo.models import Offer
from apps.volontulo.models import Organization
from apps.volontulo.models import UserProfile


class TestOffersEdit(TestCase):
    """Class responsible for testing offer's edit page."""

    @classmethod
    def setUpTestData(cls):
        """Set up data for all tests."""
        cls.organization = Organization.objects.create(
            name='Organization Name',
            address='',
            description='',
        )
        cls.organization.save()
        cls.organization_user_email = 'organization@example.com'
        cls.organization_user_password = '123org'
        organization_user = User.objects.create_user(
            cls.organization_user_email,
            cls.organization_user_email,
            cls.organization_user_password
        )
        organization_user.save()
        cls.organization_profile = UserProfile(
            user=organization_user
        )
        cls.organization_profile.save()
        # pylint: disable=no-member
        cls.organization_profile.organizations.add(cls.organization)
        cls.offer = Offer.objects.create(
            organization=cls.organization,
            description='',
            requirements='',
            time_commitment='',
            benefits='',
            location='',
            title='volontulo offer',
            time_period='',
            status_old='NEW',
            started_at='2015-10-10 21:22:23',
            finished_at='2015-12-12 11:12:13',
            offer_status='published',
            recruitment_status='open',
            action_status='ongoing',
        )
        cls.offer.save()

    def setUp(self):
        """Set up each test."""
        self.client = Client()

    def test_for_non_existing_offer(self):
        """Test if error 404 will be raised when offer dosn't exits."""
        self.client.post('/login', {
            'email': 'organization@example.com',
            'password': '123org',
        })
        response = self.client.get('/offers/some-slug/42/edit')
        self.assertEqual(response.status_code, 404)

    def test_for_different_slug(self):
        """Test if redirect will be raised when offer has different slug."""
        self.client.post('/login', {
            'email': 'organization@example.com',
            'password': '123org',
        })
        response = self.client.get(
            '/offers/different-slug/{}/edit'.format(self.offer.id))
        self.assertRedirects(
            response,
            '/offers/volontulo-offer/{}/edit'.format(self.offer.id),
            302,
            200,
        )

    def test_for_correct_slug(self):
        """Test of get request for offers/edit with correct slug."""
        self.client.post('/login', {
            'email': self.organization_user_email,
            'password': self.organization_user_password
        })
        response = self.client.get(
            '/offers/volontulo-offer/{}/edit'.format(self.offer.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_form.html')

    def test_offers_edit_invalid_form(self):
        """Test attempt of edition of offer with invalid form."""
        self.client.post('/login', {
            'email': 'organization@example.com',
            'password': '123org',
        })
        response = self.client.post('/offers/volontulo-offer/{}/edit'.format(
            self.offer.id
        ), {
            'edit_type': 'full_edit',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_form.html')
        self.assertContains(
            response,
            'Formularz zawiera niepoprawnie wypełnione pola'
        )
        offer = Offer.objects.get(id=self.offer.id)
        self.assertEqual(
            offer.organization,
            self.organization_profile.organizations.all()[0],
        )
        self.assertEqual(offer.description, '')
        self.assertEqual(offer.requirements, '')
        self.assertEqual(
            offer.time_commitment,
            ''
        )
        self.assertEqual(offer.benefits, '')
        self.assertEqual(offer.location, '')
        self.assertEqual(offer.title, 'volontulo offer')
        self.assertEqual(offer.time_period, '')

    def test_offers_edit_valid_form(self):
        """Test attempt of edition of offer with valid form."""
        self.client.post('/login', {
            'email': 'organization@example.com',
            'password': '123org',
        })
        response = self.client.post('/offers/volontulo-offer/{}/edit'.format(
            self.offer.id
        ), {
            'edit_type': 'full_edit',
            'organization': self.organization.id,
            'description': 'required description',
            'requirements': 'required requirements',
            'time_commitment': 'required time_commitment',
            'benefits': 'required benefits',
            'location': 'required location',
            'title': 'another volontulo offer',
            'time_period': 'required time_period',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_form.html')
        self.assertContains(
            response,
            'Oferta została zmieniona.'
        )
        offer = Offer.objects.get(id=self.offer.id)
        self.assertEqual(
            offer.organization,
            self.organization_profile.organizations.all()[0],
        )
        self.assertEqual(offer.description, 'required description')
        self.assertEqual(offer.requirements, 'required requirements')
        self.assertEqual(
            offer.time_commitment,
            'required time_commitment'
        )
        self.assertEqual(offer.benefits, 'required benefits')
        self.assertEqual(offer.location, 'required location')
        self.assertEqual(offer.title, 'another volontulo offer')
        self.assertEqual(offer.time_period, 'required time_period')

    def test_offers_status_change(self):
        """Test status change made using offers/edit."""
        self.client.post('/login', {
            'email': 'organization@example.com',
            'password': '123org',
        })
        response = self.client.post('/offers/volontulo-offer/{}/edit'.format(
            self.offer.id
        ), {
            'edit_type': 'status_change',
            'status_old': 'ACTIVE'
        })
        self.assertEqual(response.status_code, 200)
        offer = Offer.objects.get(id=self.offer.id)
        self.assertEqual(offer.status_old, 'NEW')
