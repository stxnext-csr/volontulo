# -*- coding: utf-8 -*-

u"""
.. module:: test_offer_view
"""

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from apps.volontulo.models import Offer
from apps.volontulo.models import Organization
from apps.volontulo.models import UserProfile


class TestOffersView(TestCase):
    """Class responsible for testing offer's view page."""

    @classmethod
    def setUpTestData(cls):
        """Set up data for all tests."""
        organization = Organization.objects.create(
            name='Organization Name',
            address='',
            description='',
        )
        organization.save()
        administrator = User.objects.create_user(
            'admin@example.com',
            'admin@example.com',
            '123admin'
        )
        administrator.save()
        cls.administrator_profile = UserProfile(
            user=administrator,
            is_administrator=True,
        )
        cls.administrator_profile.save()
        cls.offer = Offer.objects.create(
            organization=organization,
            description='',
            requirements='',
            time_commitment='',
            benefits='',
            location='',
            title='volontulo offer',
            time_period='',
            status_old='NEW',
            started_at='2105-10-24 09:10:11',
            finished_at='2105-11-28 12:13:14',
            offer_status='unpublished',
            recruitment_status='open',
            action_status='ongoing',
        )
        cls.offer.save()

        volunteers = [User.objects.create_user(
            'v{}@example.com'.format(i),
            'v{}@example.com'.format(i),
            'v{}'.format(i),
        ) for i in range(10)]
        for i in range(10):
            volunteers[i].save()
        cls.volunteers_profiles = [
            UserProfile(user=volunteers[i]) for i in range(10)
        ]
        for i in range(10):
            cls.volunteers_profiles[i].save()
        for i in range(0, 10, 2):
            cls.offer.volunteers.add(cls.volunteers_profiles[i].user)

    def setUp(self):
        """Set up each test."""
        self.client = Client()

    def test_for_non_existing_offer(self):
        """Test if error 404 will be raised when offer dosn't exist."""
        response = self.client.get('/offers/some-slug/42')
        self.assertEqual(response.status_code, 404)

    def test_for_different_slug(self):
        """Test if redirect will be raised when offer has different slug."""
        response = self.client.get('/offers/different-slug/{}'.format(
            self.offer.id))
        self.assertRedirects(
            response,
            '/offers/volontulo-offer/{}'.format(self.offer.id),
            302,
            200,
        )

    def test_for_correct_slug(self):
        """Test offer details for standard user."""
        response = self.client.get('/offers/volontulo-offer/{}'.format(
            self.offer.id
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/show_offer.html')
        self.assertIn('offer', response.context)
        self.assertIn('volunteers', response.context)
