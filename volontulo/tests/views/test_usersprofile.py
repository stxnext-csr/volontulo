# -*- coding: utf-8 -*-

u"""
.. module:: test_users
"""
from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from volontulo.models import Badge
from volontulo.models import Offer
from volontulo.models import Organization
from volontulo.models import UserBadges
from volontulo.models import UserProfile


class TestUsersProfile(TestCase):
    u"""Class responsible for testing users profile view."""

    @classmethod
    def setUpTestData(cls):
        # volunteer user - totally useless
        cls.initialize_empty_volunteer()
        # organization user - no offers
        cls.initialize_empty_organization()
        # volunteer user - badges, offers, organizations
        cls.initialize_filled_volunteer_and_organization()

    @classmethod
    def initialize_empty_volunteer(cls):
        u"""Initialize empty volunteer."""
        volunteer_user1 = User.objects.create_user(
            'volunteer1@example.com',
            'volunteer1@example.com',
            'volunteer1'
        )
        volunteer_user1.save()
        cls.user_profile1 = UserProfile.objects.create(user=volunteer_user1)

    @classmethod
    def initialize_empty_organization(cls):
        u"""Initialize empty organization."""
        organization1 = Organization.objects.create(name=u'Organization 1')
        organization1.save()
        organization_user1 = User.objects.create_user(
            'organization1@example.com',
            'organization1@example.com',
            'organization1'
        )
        organization_user1.save()
        cls.organization_profile1 = UserProfile.objects.create(
            user=organization_user1,
        )
        cls.organization_profile1.organizations.add(organization1)

    @classmethod
    # pylint: disable=invalid-name
    def initialize_filled_volunteer_and_organization(cls):
        u"""Initialize volunteer filled with data."""
        # create volunteer user
        volunteer_user2 = User.objects.create_user(
            'volunteer2@example.com',
            'volunteer2@example.com',
            'volunteer2'
        )
        volunteer_user2.save()
        cls.user_profile2 = UserProfile.objects.create(user=volunteer_user2)

        # create 3 badges with different priorities
        for i in range(1, 4):
            badge = Badge.objects.create(
                name='Badge {}'.format(i),
                slug='badge-{}'.format(i),
                priority=i,
            )
            badge.save()
            usersbadge = UserBadges.objects.create(
                userprofile=cls.user_profile2,
                badge=badge,
                counter=i,
            )
            usersbadge.save()

        # create organization user to create offers
        organization2 = Organization.objects.create(name=u'Organization 2')
        organization2.save()
        # this is required due to login to this user
        organization_user2 = User.objects.create_user(
            'organization2@example.com',
            'organization2@example.com',
            'organization2'
        )
        organization_user2.save()
        cls.organization_profile2 = UserProfile.objects.create(
            user=organization_user2,
        )
        cls.organization_profile2.organizations.add(organization2)

        # create organization offers and assign volunteer to them
        for i in range(1, 6):
            offer = Offer.objects.create(
                title=u'Title {}'.format(i),
                description=u'Description {}'.format(i),
                requirements=u'Requirements {}'.format(i),
                time_commitment=u'Time commitment {}'.format(i),
                benefits=u'Benefits {}'.format(i),
                location=u'Location {}'.format(i),
                time_period=u'Time period {}'.format(i),
                status=u'ACTIVE',
                votes=True,
                organization=organization2,
            )
            offer.volunteers.add(volunteer_user2)
            offer.save()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    # pylint: disable=invalid-name
    def test__logged_user_profile_anonymous(self):
        u"""Testing user profile page for anonymous"""
        response = self.client.get('/me')

        self.assertEqual(response.status_code, 302)

    # pylint: disable=invalid-name
    def test__logged_user_profile(self):
        u"""Testing default views on user profile form"""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/me')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_profile.html')
        # check if contain image upload form (all users)
        # pylint: disable=no-member
        self.assertIn('image', response.context)
        self.assertContains(response, u'Wybierz grafikę')

    # pylint: disable=invalid-name
    def test__logged_user_profile_empty_volunteer(self):
        u"""Testing user profile page for volunteers"""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/me')

        self.assertContains(response, u'Jako wolontariusz chciałbym')
        # pylint: disable=no-member
        self.assertIn('badges', response.context)
        self.assertContains(response, u'Nie masz jeszcze żadnych odznak')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        self.assertContains(
            response,
            u'Nie wyraziłeś chęci udziału w żadnej z dostępnych ofert.'
        )

    # pylint: disable=invalid-name
    def test__logged_user_profile_filled_volunteer(self):
        u"""Testing user profile page for volunteers"""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/me')

        self.assertContains(response, u'Jako wolontariusz chciałbym')
        # pylint: disable=no-member
        self.assertIn('badges', response.context)
        self.assertContains(response, u'Nie masz jeszcze żadnych odznak')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        self.assertContains(
            response,
            u'Nie wyraziłeś chęci udziału w żadnej z dostępnych ofert.'
        )

    # pylint: disable=invalid-name
    def test__logged_user_profile_empty_organization(self):
        u"""Testing user profile page for empty organization"""
        self.client.post('/login', {
            'email': u'organization1@example.com',
            'password': 'organization1',
        })
        response = self.client.get('/me')

        self.assertContains(response, u'Jako organizacja chciałbym')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        self.assertContains(
            response,
            u'Ta organizacja nie ma jeszcze żadnych ofert.'
        )

    # pylint: disable=invalid-name
    def test__logged_user_profile_filled_organization(self):
        u"""Testing user profile page for filled organization"""
        self.client.post('/login', {
            'email': u'organization2@example.com',
            'password': 'organization2',
        })
        response = self.client.get('/me')

        self.assertContains(response, u'Jako organizacja chciałbym')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        self.assertEqual(
            5,
            Offer.objects.all().count()
        )
        self.assertNotContains(
            response,
            u'Ta organizacja nie ma jeszcze żadnych ofert.'
        )
