# -*- coding: utf-8 -*-

u"""
.. module:: test_offer_join
"""

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from apps.volontulo.models import Offer
from apps.volontulo.models import Organization
from apps.volontulo.models import UserProfile


class TestOffersJoin(TestCase):
    """Class responsible for testing offer's join page."""

    @classmethod
    def setUpTestData(cls):
        """Set up data for all tests."""
        organization = Organization.objects.create(
            name='Organization Name',
            address='',
            description='',
        )
        organization.save()

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
            started_at='2015-10-10 21:22:23',
            finished_at='2015-12-12 11:12:13',
        )
        cls.offer.save()

        cls.volunteer = User.objects.create_user(
            'volunteer@example.com',
            'volunteer@example.com',
            'vol123',
        )
        cls.volunteer.save()
        cls.volunteer_profile = UserProfile(user=cls.volunteer)
        cls.volunteer_profile.save()

    def setUp(self):
        """Set up each test."""
        self.client = Client()

    def test_for_nonexisting_offer(self):
        """Test if error 404 will be raised when offer dosn't exist."""
        response = self.client.get('/offers/some-slug/42/join')
        self.assertEqual(response.status_code, 404)

    def test_for_different_slug(self):
        """Test if redirect will be raised when offer has different slug."""
        response = self.client.get('/offers/different-slug/{}/join'.format(
            self.offer.id
        ))
        self.assertRedirects(
            response,
            '/offers/volontulo-offer/{}/join'.format(self.offer.id),
            302,
            200,
        )

    # pylint: disable=invalid-name
    def test_correct_slug_for_anonymous_user(self):
        """Test get method of offer join for anonymous user."""
        response = self.client.get('/offers/volontulo-offer/{}/join'.format(
            self.offer.id
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_apply.html')
        # pylint: disable=no-member
        self.assertIn('offer', response.context)
        self.assertIn('volunteer_user', response.context)
        self.assertEqual(response.context['volunteer_user'].pk, None)

    # pylint: disable=invalid-name
    def test_correct_slug_for_logged_in_user(self):
        """Test get method of offer join for logged in user."""
        self.client.post('/login', {
            'email': 'volunteer@example.com',
            'password': 'vol123',
        })
        response = self.client.get('/offers/volontulo-offer/{}/join'.format(
            self.offer.id
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_apply.html')
        # pylint: disable=no-member
        self.assertIn('offer', response.context)
        self.assertIn('volunteer_user', response.context)
        self.assertEqual(response.context['volunteer_user'].pk,
                         self.volunteer_profile.id)
        self.assertContains(response, 'volunteer@example.com')

    def test_offers_join_invalid_form(self):
        """Test attempt of joining offer with invalid form."""
        response = self.client.post('/offers/volontulo-offer/{}/join'.format(
            self.offer.id
        ), {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_apply.html')
        self.assertContains(
            response,
            'Formularz zawiera nieprawidłowe dane',
        )

    def test_offers_join_valid_form_and_logged_user(self):
        """Test attempt of joining offer with valid form and logged user."""
        self.client.post('/login', {
            'email': 'volunteer@example.com',
            'password': 'vol123',
        })

        # successfull joining offer:
        response = self.client.post('/offers/volontulo-offer/{}/join'.format(
            self.offer.id
        ), {
            'email': 'volunteer@example.com',
            'phone_no': '+42 42 42 42',
            'fullname': 'Mister Volunteer',
            'comments': 'Some important staff.',
        }, follow=True)
        self.assertRedirects(
            response,
            '/offers/volontulo-offer/{}'.format(self.offer.id),
            302,
            200,
        )

        # unsuccessfull joining the same offer for the second time:
        response = self.client.post('/offers/volontulo-offer/{}/join'.format(
            self.offer.id
        ), {
            'email': 'volunteer@example.com',
            'phone_no': '+42 42 42 42',
            'fullname': 'Mister Volunteer',
            'comments': 'Some important staff.',
        }, follow=True)
        self.assertRedirects(
            response,
            '/offers',
            302,
            200,
        )
        self.assertContains(
            response,
            'Już wyraziłeś chęć uczestnictwa w tej ofercie.',
        )

    def test_offers_join_valid_form_and_anonymous_user(self):
        """Test attempt of joining offer with valid form and anon user."""
        post_data = {
            'email': 'anon@example.com',
            'phone_no': '+42 42 42 42',
            'fullname': 'Mister Anonymous',
            'comments': 'Some important staff.',
        }

        # successfull joining offer:
        response = self.client.post(
            '/offers/volontulo-offer/{}/join'.format(self.offer.id),
            post_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            '/register',
            302,
            200,
        )
        self.assertContains(
            response,
            'Zarejestruj się, aby zapisać się do oferty.',
        )

    def test_offers_join_valid_form_with_existing_email(self):
        """Test attempt of joining offer with valid form and existing email."""
        post_data = {
            'email': 'volunteer@example.com',
            'phone_no': '+42 42 42 42',
            'fullname': 'Mister Anonymous',
            'comments': 'Some important staff.',
        }

        # successfull joining offer:
        response = self.client.post(
            '/offers/volontulo-offer/{}/join'.format(self.offer.id),
            post_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            '/login?next=/offers/volontulo-offer/{}/join'.format(
                self.offer.id
            ),
            302,
            200,
        )
        self.assertContains(
            response,
            'Zaloguj się, aby zapisać się do oferty.',
        )
