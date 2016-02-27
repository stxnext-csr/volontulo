# -*- coding: utf-8 -*-

u"""
.. module:: test_offers
"""

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from apps.volontulo.models import (
    Offer, Organization, UserProfile
)


class TestOffersList(TestCase):
    u"""Class responsible for testing offers' list."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        cls.organization = Organization.objects.create(
            name='Organization Name',
            address='',
            description='',
        )
        cls.organization.save()

        common_offer_data = {
            'organization': cls.organization,
            'description': '',
            'requirements': '',
            'time_commitment': '',
            'benefits': '',
            'location': '',
            'title': 'volontulo offer',
            'time_period': '',
            'started_at': '2105-10-24 09:10:11',
            'finished_at': '2105-11-28 12:13:14',
            'offer_status': 'unpublished',
            'recruitment_status': 'closed',
            'action_status': 'ongoing',
        }

        cls.inactive_offer = Offer.objects.create(
            status_old='NEW',
            **common_offer_data
        )
        cls.inactive_offer.save()
        cls.active_offer = Offer.objects.create(
            status_old='ACTIVE',
            **common_offer_data
        )
        cls.active_offer.save()

        volunteer_user = User.objects.create_user(
            'volunteer@example.com',
            'volunteer@example.com',
            '123volunteer'
        )
        volunteer_user.save()
        cls.volunteer = UserProfile(user=volunteer_user)
        cls.volunteer.save()

        organization_user = User.objects.create_user(
            'cls.organization@example.com',
            'cls.organization@example.com',
            '123org'
        )
        organization_user.save()
        cls.organization_profile = UserProfile(
            user=organization_user,
        )
        cls.organization_profile.save()
        # pylint: disable=no-member
        cls.organization_profile.organizations.add(cls.organization)

        admin_user = User.objects.create_user(
            'admin@example.com',
            'admin@example.com',
            '123admin'
        )
        admin_user.save()
        cls.admin = UserProfile(
            user=admin_user,
            is_administrator=True,
        )
        cls.admin.save()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    # pylint: disable=invalid-name
    def _test_offers_list_for_standard_user(self):
        u"""Test offers' list for standard user.

        List of offers is available for standard users and shows only ACTIVE
        offers.
        Test are common for anonymous user, volunteer and organization.
        """
        response = self.client.get('/offers')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offers_list.html')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        # pylint: disable=no-member
        self.assertEqual(len(response.context['offers']), 0)

    def test_offer_list_for_anonymous_user(self):
        u"""Test offers' list for anonymus user."""
        return self._test_offers_list_for_standard_user()

    def test_offers_list_for_volunteer(self):
        u"""Test offers' list for account of volunteer."""
        self.client.post('/login', {
            'email': 'volunteer@example.com',
            'password': '123volunteer',
        })
        return self._test_offers_list_for_standard_user()

    def test_offers_list_for_organization(self):
        u"""Test offers' list for account of organization."""
        self.client.post('/login', {
            'email': 'organization@example.com',
            'password': '123org',
        })
        return self._test_offers_list_for_standard_user()

    def test_offers_list_for_admin(self):
        """Test offers' list for account of admin."""
        self.client.post('/login', {
            'email': 'admin@example.com',
            'password': '123admin',
        })
        response = self.client.get('/offers')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offers_list.html')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        # pylint: disable=no-member
        self.assertEqual(len(response.context['offers']), 2)


class TestOfferDelete(TestCase):
    """Class responsible for testing offers deletion."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        cls.organization = Organization.objects.create(
            name='',
            address='',
            description='',
        )

        common_offer_data = {
            'organization': cls.organization,
            'description': '',
            'requirements': '',
            'time_commitment': '',
            'benefits': '',
            'location': '',
            'title': 'volontulo offer',
            'time_period': '',
            'started_at': '2105-10-24 09:10:11',
            'finished_at': '2105-11-28 12:13:14',
            'offer_status': 'unpublished',
            'recruitment_status': 'closed',
            'action_status': 'ongoing',
        }

        cls.inactive_offer = Offer.objects.create(
            status_old='NEW',
            **common_offer_data
        )

        cls.active_offer = Offer.objects.create(
            status_old='ACTIVE',
            **common_offer_data
        )

        volunteer_user = User.objects.create_user(
            'volunteer@example.com',
            'volunteer@example.com',
            '123volunteer'
        )

        cls.volunteer = UserProfile(user=volunteer_user)
        cls.volunteer.save()

        organization_user = User.objects.create_user(
            'cls.organization@example.com',
            'cls.organization@example.com',
            '123org'
        )

        cls.organization_profile = UserProfile(
            user=organization_user,
        )
        cls.organization_profile.save()
        # pylint: disable=no-member
        cls.organization_profile.organizations.add(cls.organization)

        admin_user = User.objects.create_user(
            'admin@example.com',
            'admin@example.com',
            '123admin'
        )

        cls.admin = UserProfile(
            user=admin_user,
            is_administrator=True,
        )
        cls.admin.save()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    # pylint: disable=invalid-name
    def test_offer_deletion_for_anonymous_user(self):
        """Test deletion for anonymous users"""
        response = self.client.get('/offers/delete/{}'
                                   .format(self.inactive_offer.id))
        self.assertEqual(response.status_code, 403)

    # pylint: disable=invalid-name
    def test_offer_deletion_for_volunteer(self):
        u"""Test deletion for account of volunteer."""
        self.client.post('/login', {
            'email': 'volunteer@example.com',
            'password': '123volunteer',
        })
        response = self.client.get('/offers/delete/{}'
                                   .format(self.inactive_offer.id))
        self.assertEqual(response.status_code, 403)

    # pylint: disable=invalid-name
    def test_offer_deletion_for_organization(self):
        u"""Test deletion for account of organization."""
        self.client.post('/login', {
            'email': 'organization@example.com',
            'password': '123org',
        })
        response = self.client.get('/offers/delete/{}'
                                   .format(self.inactive_offer.id))
        self.assertEqual(response.status_code, 403)

    # pylint: disable=invalid-name
    def test_offer_deletion_for_admin(self):
        """Test deletion for account of admin."""
        self.client.post('/login', {
            'email': 'admin@example.com',
            'password': '123admin',
        })
        response = self.client.get('/offers/delete/{}'
                                   .format(self.inactive_offer.id))
        self.assertEqual(response.status_code, 302)


class TestOfferAccept(TestCase):
    """Class responsible for testing offers acceptance."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        cls.organization = Organization.objects.create(
            name='',
            address='',
            description='',
        )

        common_offer_data = {
            'organization': cls.organization,
            'description': '',
            'requirements': '',
            'time_commitment': '',
            'benefits': '',
            'location': '',
            'title': 'volontulo offer',
            'time_period': '',
            'started_at': '2105-10-24 09:10:11',
            'finished_at': '2105-11-28 12:13:14',
            'offer_status': 'unpublished',
            'recruitment_status': 'closed',
            'action_status': 'ongoing',
        }

        cls.inactive_offer = Offer.objects.create(
            status_old='NEW',
            **common_offer_data
        )
        cls.inactive_offer.save()
        cls.active_offer = Offer.objects.create(
            status_old='ACTIVE',
            **common_offer_data
        )

        volunteer_user = User.objects.create_user(
            'volunteer@example.com',
            'volunteer@example.com',
            '123volunteer'
        )

        cls.volunteer = UserProfile(user=volunteer_user)
        cls.volunteer.save()

        organization_user = User.objects.create_user(
            'cls.organization@example.com',
            'cls.organization@example.com',
            '123org'
        )

        cls.organization_profile = UserProfile(
            user=organization_user,
        )
        cls.organization_profile.save()
        # pylint: disable=no-member
        cls.organization_profile.organizations.add(cls.organization)

        admin_user = User.objects.create_user(
            'admin@example.com',
            'admin@example.com',
            '123admin'
        )
        cls.admin = UserProfile(
            user=admin_user,
            is_administrator=True,
        )
        cls.admin.save()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    # pylint: disable=invalid-name
    def test_offer_acceptance_for_anonymous_user(self):
        """Test offer acceptance for anonymous users"""
        response = self.client.get('/offers/delete/{}'
                                   .format(self.inactive_offer.id))
        self.assertEqual(response.status_code, 403)

    # pylint: disable=invalid-name
    def test_offer_acceptance_for_volunteer(self):
        u"""Test offer acceptance for account of volunteer."""
        self.client.post('/login', {
            'email': 'volunteer@example.com',
            'password': '123volunteer',
        })
        response = self.client.get('/offers/delete/{}'
                                   .format(self.inactive_offer.id))
        self.assertEqual(response.status_code, 403)

    # pylint: disable=invalid-name
    def test_offer_acceptance_for_organization(self):
        u"""Test offer acceptance for account of organization."""
        self.client.post('/login', {
            'email': 'organization@example.com',
            'password': '123org',
        })
        response = self.client.get('/offers/delete/{}'
                                   .format(self.inactive_offer.id))
        self.assertEqual(response.status_code, 403)

    # pylint: disable=invalid-name
    def test_offer_acceptance_for_admin(self):
        """Test offer acceptance for account of admin."""
        self.client.post('/login', {
            'email': 'admin@example.com',
            'password': '123admin',
        })
        response = self.client.get('/offers/delete/{}'
                                   .format(self.inactive_offer.id))
        self.assertEqual(response.status_code, 302)


class TestOffersCreate(TestCase):
    u"""Class responsible for testing offer's create page."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
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
            u'no_organ@example.com',
            u'no_organ@example.com',
            u'123no_org'
        )
        UserProfile.objects.create(
            user=no_org_user,
        )

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    def test_offers_create_get_method(self):
        u"""Test page for offer creation - tendering template with form."""
        self.client.post('/login', {
            'email': 'organization@example.com',
            'password': '123org',
        })
        response = self.client.get('/offers/create')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_form.html')

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
        u"""Test attempt of creation of new offer with invalid form."""
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
            'email': u'organization@example.com',
            'password': '123org',
        })

        response = self.client.post('/offers/create', {
            'organization': self.organization.id,
            'description': 'desc',
            'requirements': u'required requirements',
            'time_commitment': u'required time_commitment',
            'benefits': u'required benefits',
            'location': u'required location',
            'title': u'volontulo offer',
            'time_period': u'required time_period',
            'started_at': '',
            'finished_at': '',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        offer = Offer.objects.get(description='desc')
        self.assertEqual(offer.action_status, 'ongoing')

    def test_offers_create_valid_form(self):
        u"""Test attempt of creation of new offer with valid form."""
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
