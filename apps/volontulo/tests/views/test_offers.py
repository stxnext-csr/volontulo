# -*- coding: utf-8 -*-

u"""
.. module:: test_offers
"""

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from apps.volontulo.models import Offer
from apps.volontulo.models import Organization
from apps.volontulo.models import UserProfile


class TestOffersList(TestCase):
    u"""Class responsible for testing offers' list."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        cls.organization = Organization.objects.create(
            name=u'',
            address=u'',
            description=u'',
        )
        cls.organization.save()

        common_offer_data = {
            'organization': cls.organization,
            'description': u'',
            'requirements': u'',
            'time_commitment': u'',
            'benefits': u'',
            'location': u'',
            'title': u'volontulo offer',
            'time_period': u'',
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
            u'volunteer@example.com',
            u'volunteer@example.com',
            u'123volunteer'
        )
        volunteer_user.save()
        cls.volunteer = UserProfile(user=volunteer_user)
        cls.volunteer.save()

        organization_user = User.objects.create_user(
            u'cls.organization@example.com',
            u'cls.organization@example.com',
            u'123org'
        )
        organization_user.save()
        cls.organization_profile = UserProfile(
            user=organization_user,
        )
        cls.organization_profile.save()
        # pylint: disable=no-member
        cls.organization_profile.organizations.add(cls.organization)

        admin_user = User.objects.create_user(
            u'admin@example.com',
            u'admin@example.com',
            u'123admin'
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
            'email': u'volunteer@example.com',
            'password': '123volunteer',
        })
        return self._test_offers_list_for_standard_user()

    def test_offers_list_for_organization(self):
        u"""Test offers' list for account of organization."""
        self.client.post('/login', {
            'email': u'organization@example.com',
            'password': '123org',
        })
        return self._test_offers_list_for_standard_user()

    def test_offers_list_for_admin(self):
        u"""Test offers' list for account of admin."""
        self.client.post('/login', {
            'email': u'admin@example.com',
            'password': '123admin',
        })
        response = self.client.get('/offers')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offers_list.html')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        # pylint: disable=no-member
        self.assertEqual(len(response.context['offers']), 2)


class TestOffersCreate(TestCase):
    u"""Class responsible for testing offer's create page."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        cls.organization = Organization.objects.create(
            name=u'',
            address=u'',
            description=u'',
        )
        cls.organization.save()
        organization_user = User.objects.create_user(
            u'organization@example.com',
            u'organization@example.com',
            u'123org'
        )
        organization_user.save()
        cls.organization_profile = UserProfile(
            user=organization_user,
        )
        cls.organization_profile.save()
        # pylint: disable=no-member
        cls.organization_profile.organizations.add(cls.organization)

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    def test_offers_create_get_method(self):
        u"""Test page for offer creation - tendering template with form."""
        self.client.post('/login', {
            'email': u'organization@example.com',
            'password': '123org',
        })
        response = self.client.get('/offers/create')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_form.html')

    def test_offers_create_invalid_form(self):
        u"""Test attempt of creation of new offer with invalid form."""
        self.client.post('/login', {
            'email': u'organization@example.com',
            'password': '123org',
        })
        response = self.client.post('/offers/create', {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_form.html')
        self.assertContains(
            response,
            u'Formularz zawiera niepoprawnie wypełnione pola'
        )

    def test_offers_create_valid_form(self):
        u"""Test attempt of creation of new offer with valid form."""
        self.client.post('/login', {
            'email': u'organization@example.com',
            'password': '123org',
        })
        for i in range(1, 4):
            response = self.client.post('/offers/create', {
                'organization': self.organization.id,
                'description': str(i),
                'requirements': u'required requirements',
                'time_commitment': u'required time_commitment',
                'benefits': u'required benefits',
                'location': u'required location',
                'title': u'volontulo offer',
                'time_period': u'required time_period',
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
            self.assertEqual(offer.requirements, u'required requirements')
            self.assertEqual(
                offer.time_commitment,
                u'required time_commitment'
            )
            self.assertEqual(offer.benefits, u'required benefits')
            self.assertEqual(offer.location, u'required location')
            self.assertEqual(offer.title, u'volontulo offer')
            self.assertEqual(offer.time_period, u'required time_period')


class TestOffersEdit(TestCase):
    u"""Class responsible for testing offer's edit page."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        cls.organization = Organization.objects.create(
            name=u'',
            address=u'',
            description=u'',
        )
        cls.organization.save()
        cls.organization_user_email = u'organization@example.com'
        cls.organization_user_password = u'123org'
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
            description=u'',
            requirements=u'',
            time_commitment=u'',
            benefits=u'',
            location=u'',
            title=u'volontulo offer',
            time_period=u'',
            status_old='NEW',
            started_at='2015-10-10 21:22:23',
            finished_at='2015-12-12 11:12:13',
            offer_status='published',
            recruitment_status='open',
            action_status='ongoing',
        )
        cls.offer.save()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    def test_for_non_existing_offer(self):
        u"""Test if error 404 will be raised when offer dosn't exits."""
        self.client.post('/login', {
            'email': u'organization@example.com',
            'password': '123org',
        })
        response = self.client.get('/offers/some-slug/42/edit')
        self.assertEqual(response.status_code, 404)

    def test_for_different_slug(self):
        u"""Test if redirect will be raised when offer has different slug."""
        self.client.post('/login', {
            'email': u'organization@example.com',
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
        u"""Test of get request for offers/edit with correct slug."""
        self.client.post('/login', {
            'email': self.organization_user_email,
            'password': self.organization_user_password
        })
        response = self.client.get(
            '/offers/volontulo-offer/{}/edit'.format(self.offer.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_form.html')

    def test_offers_edit_invalid_form(self):
        u"""Test attempt of edition of offer with invalid form."""
        self.client.post('/login', {
            'email': u'organization@example.com',
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
            u'Formularz zawiera niepoprawnie wypełnione pola'
        )
        offer = Offer.objects.get(id=self.offer.id)
        self.assertEqual(
            offer.organization,
            self.organization_profile.organizations.all()[0],
        )
        self.assertEqual(offer.description, u'')
        self.assertEqual(offer.requirements, u'')
        self.assertEqual(
            offer.time_commitment,
            u''
        )
        self.assertEqual(offer.benefits, u'')
        self.assertEqual(offer.location, u'')
        self.assertEqual(offer.title, u'volontulo offer')
        self.assertEqual(offer.time_period, u'')

    def test_offers_edit_valid_form(self):
        u"""Test attempt of edition of offer with valid form."""
        self.client.post('/login', {
            'email': u'organization@example.com',
            'password': '123org',
        })
        response = self.client.post('/offers/volontulo-offer/{}/edit'.format(
            self.offer.id
        ), {
            'edit_type': 'full_edit',
            'organization': self.organization.id,
            'description': u'required description',
            'requirements': u'required requirements',
            'time_commitment': u'required time_commitment',
            'benefits': u'required benefits',
            'location': u'required location',
            'title': u'another volontulo offer',
            'time_period': u'required time_period',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_form.html')
        self.assertContains(
            response,
            u'Oferta została zmieniona.'
        )
        offer = Offer.objects.get(id=self.offer.id)
        self.assertEqual(
            offer.organization,
            self.organization_profile.organizations.all()[0],
        )
        self.assertEqual(offer.description, u'required description')
        self.assertEqual(offer.requirements, u'required requirements')
        self.assertEqual(
            offer.time_commitment,
            u'required time_commitment'
        )
        self.assertEqual(offer.benefits, u'required benefits')
        self.assertEqual(offer.location, u'required location')
        self.assertEqual(offer.title, u'another volontulo offer')
        self.assertEqual(offer.time_period, u'required time_period')

    def test_offers_status_change(self):
        u"""Test status change made using offers/edit."""
        self.client.post('/login', {
            'email': u'organization@example.com',
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
        self.assertEqual(offer.status_old, u'NEW')


class TestOffersView(TestCase):
    u"""Class responsible for testing offer's view page."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        organization = Organization.objects.create(
            name=u'',
            address=u'',
            description=u'',
        )
        organization.save()
        administrator = User.objects.create_user(
            u'admin@example.com',
            u'admin@example.com',
            u'123admin'
        )
        administrator.save()
        cls.administrator_profile = UserProfile(
            user=administrator,
            is_administrator=True,
        )
        cls.administrator_profile.save()
        cls.offer = Offer.objects.create(
            organization=organization,
            description=u'',
            requirements=u'',
            time_commitment=u'',
            benefits=u'',
            location=u'',
            title=u'volontulo offer',
            time_period=u'',
            status_old='NEW',
            started_at='2105-10-24 09:10:11',
            finished_at='2105-11-28 12:13:14',
            offer_status='unpublished',
            recruitment_status='open',
            action_status='ongoing',
        )
        cls.offer.save()

        volunteers = [User.objects.create_user(
            u'v{}@example.com'.format(i),
            u'v{}@example.com'.format(i),
            u'v{}'.format(i),
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
        u"""Set up each test."""
        self.client = Client()

    def test_for_non_existing_offer(self):
        u"""Test if error 404 will be raised when offer dosn't exist."""
        response = self.client.get('/offers/some-slug/42')
        self.assertEqual(response.status_code, 404)

    def test_for_different_slug(self):
        u"""Test if redirect will be raised when offer has different slug."""
        response = self.client.get('/offers/different-slug/{}'.format(
            self.offer.id))
        self.assertRedirects(
            response,
            '/offers/volontulo-offer/{}'.format(self.offer.id),
            302,
            200,
        )

    def test_for_correct_slug(self):
        u"""Test offer details for standard user."""
        response = self.client.get('/offers/volontulo-offer/{}'.format(
            self.offer.id
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/show_offer.html')
        # pylint: disable=no-member
        self.assertIn('offer', response.context)
        self.assertIn('volunteers', response.context)


class TestOffersJoin(TestCase):
    u"""Class responsible for testing offer's join page."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        organization = Organization.objects.create(
            name=u'',
            address=u'',
            description=u'',
        )
        organization.save()

        cls.offer = Offer.objects.create(
            organization=organization,
            description=u'',
            requirements=u'',
            time_commitment=u'',
            benefits=u'',
            location=u'',
            title=u'volontulo offer',
            time_period=u'',
            status_old='NEW',
            started_at='2015-10-10 21:22:23',
            finished_at='2015-12-12 11:12:13',
        )
        cls.offer.save()

        cls.volunteer = User.objects.create_user(
            u'volunteer@example.com',
            u'volunteer@example.com',
            u'vol123',
        )
        cls.volunteer.save()
        cls.volunteer_profile = UserProfile(user=cls.volunteer)
        cls.volunteer_profile.save()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    def test_for_nonexisting_offer(self):
        u"""Test if error 404 will be raised when offer dosn't exist."""
        response = self.client.get('/offers/some-slug/42/join')
        self.assertEqual(response.status_code, 404)

    def test_for_different_slug(self):
        u"""Test if redirect will be raised when offer has different slug."""
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
        u"""Test get method of offer join for anonymous user."""
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
        u"""Test get method of offer join for logged in user."""
        self.client.post('/login', {
            'email': u'volunteer@example.com',
            'password': u'vol123',
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
        self.assertContains(response, u'volunteer@example.com')

    def test_offers_join_invalid_form(self):
        u"""Test attempt of joining offer with invalid form."""
        response = self.client.post('/offers/volontulo-offer/{}/join'.format(
            self.offer.id
        ), {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_apply.html')
        self.assertContains(
            response,
            u'Formularz zawiera nieprawidłowe dane',
        )

    def test_offers_join_valid_form_and_logged_user(self):
        u"""Test attempt of joining offer with valid form and logged user."""
        self.client.post('/login', {
            'email': u'volunteer@example.com',
            'password': u'vol123',
        })

        # successfull joining offer:
        response = self.client.post('/offers/volontulo-offer/{}/join'.format(
            self.offer.id
        ), {
            'email': u'volunteer@example.com',
            'phone_no': u'+42 42 42 42',
            'fullname': u'Mister Volunteer',
            'comments': u'Some important staff.',
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
            'email': u'volunteer@example.com',
            'phone_no': u'+42 42 42 42',
            'fullname': u'Mister Volunteer',
            'comments': u'Some important staff.',
        }, follow=True)
        self.assertRedirects(
            response,
            '/offers',
            302,
            200,
        )
        self.assertContains(
            response,
            u'Już wyraziłeś chęć uczestnictwa w tej ofercie.',
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


class TestOffersArchived(TestCase):
    u"""Class responsible for testing archived offers page."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        for i in range(1, 6):
            Organization.objects.create(
                name=u'Organization {0} name'.format(i),
                address=u'Organization {0} address'.format(i),
                description=u'Organization {0} description'.format(i),
            )

        organizations = Organization.objects.all()
        for idx, org in enumerate(organizations):
            for i in range(1, 6):
                user = User.objects.create_user(
                    u'volunteer{0}{1}@example.com'.format(idx + 1, i),
                    u'volunteer{0}{1}@example.com'.format(idx + 1, i),
                    u'password',
                )
                userprofile = UserProfile(user=user)
                userprofile.save()
                userprofile.organizations.add(org)
                userprofile.save()

        for idx, org in enumerate(organizations):
            for i in range(0, idx + 1):
                Offer.objects.create(
                    organization=org,
                    benefits=u'Offer {0}-{1} benefits'.format(idx + 1, i),
                    location=u'Offer {0}-{1} location'.format(idx + 1, i),
                    title=u'Offer {0}-{1} title'.format(idx + 1, i),
                    time_period=u'',
                    description=u'',
                    requirements=u'',
                    time_commitment=u'',
                    offer_status='published',
                    recruitment_status='closed',
                    action_status='finished',
                    started_at='2010-10-10 10:10:10',
                    finished_at='2012-12-12 12:12:12'
                )

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    def test_offers_archived_page(self):
        u"""Offers archive page."""
        response = self.client.get('/offers/archived')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/archived.html')
        # pylint: disable=no-member
        self.assertIn('offers', response.context)
        self.assertEqual(len(response.context['offers']), 15)
        self.assertNotContains(
            response,
            u'Brak ofert spełniających podane kryteria',
        )
