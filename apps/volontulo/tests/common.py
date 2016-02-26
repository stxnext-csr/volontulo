# -*- coding: utf-8 -*-

u"""
.. module:: common
"""

from django.contrib.auth.models import User

from apps.volontulo.models import Offer
from apps.volontulo.models import Organization
from apps.volontulo.models import UserProfile

COMMON_OFFER_DATA = {
    'organization': None,
    'description': u'',
    'requirements': u'',
    'time_commitment': u'',
    'benefits': u'',
    'location': u'',
    'title': u'volontulo offer',
    'time_period': u''
}


def initialize_empty_volunteer():
    u"""Initialize empty volunteer."""
    volunteer_user1 = User.objects.create_user(
        'volunteer1@example.com',
        'volunteer1@example.com',
        'volunteer1',
        first_name=u'Grzegorz',
        last_name=u'Brzęczyszczykiewicz',
    )
    volunteer_user1.save()
    userprofile = UserProfile.objects.create(user=volunteer_user1)
    userprofile.phone_no = '333666999'
    userprofile.save()
    return volunteer_user1


def initialize_empty_organization():
    u"""Initialize empty organization."""
    organization1 = Organization.objects.create(
        name=u'Organization 1',
        address=u'Organization 1 address',
        description=u'Organization 1 description',
    )
    organization1.save()
    organization_user1 = User.objects.create_user(
        'organization1@example.com',
        'organization1@example.com',
        'organization1',
        first_name=u'Organization1Firstname',
        last_name=u'Organization1Lastname',
    )
    organization_user1.save()
    organization_profile1 = UserProfile.objects.create(
        user=organization_user1,
    )
    organization_profile1.organizations.add(organization1)
    return organization1


# pylint: disable=invalid-name
def initialize_filled_volunteer_and_organization():
    u"""Initialize volunteer filled with data."""
    # create volunteer user
    volunteer_user2 = User.objects.create_user(
        'volunteer2@example.com',
        'volunteer2@example.com',
        'volunteer2'
    )
    volunteer_user2.save()

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
    organization_profile2 = UserProfile.objects.create(
        user=organization_user2,
    )
    organization_profile2.organizations.add(organization2)

    # create organization offers and assign volunteer to them
    for i in range(11, 15):
        offer = Offer.objects.create(
            title=u'Title {}'.format(i),
            description=u'Description {}'.format(i),
            requirements=u'Requirements {}'.format(i),
            time_commitment=u'Time commitment {}'.format(i),
            benefits=u'Benefits {}'.format(i),
            location=u'Location {}'.format(i),
            time_period=u'Time period {}'.format(i),
            status_old=u'ACTIVE',
            votes=True,
            started_at='2015-10-05 09:10:11',
            finished_at='2015-12-12 12:13:14',
            organization=organization2,
            offer_status='published',
            recruitment_status='open',
            action_status='ongoing',
        )
        offer.volunteers.add(volunteer_user2)
        offer.save()

    # create additional organization offers for administrator use
    for i in range(100, 110):
        offer2 = Offer.objects.create(
            title=u'Title {}'.format(i),
            description=u'Description {}'.format(i),
            requirements=u'Requirements {}'.format(i),
            time_commitment=u'Time commitment {}'.format(i),
            benefits=u'Benefits {}'.format(i),
            location=u'Location {}'.format(i),
            time_period=u'Time period {}'.format(i),
            status_old=u'SUSPENDED' if i % 2 == 0 else u'NEW',
            votes=True,
            started_at='2015-10-05 09:10:11',
            finished_at='2015-12-12 12:13:14',
            organization=organization2,
            offer_status='unpublished',
            recruitment_status='open',
            action_status='ongoing',
        )
        offer2.save()

    return volunteer_user2, organization2


def initialize_empty_organizations():
    u"""Initialize empty organization."""
    for i in range(11, 15):
        organization = Organization.objects.create(
            id=i,
            name=u'Organization {}'.format(i)
        )
        organization.save()
        organization_user = User.objects.create_user(
            'organization{}@example.com'.format(i),
            'organization{}@example.com'.format(i),
            'organization{}'.format(i)
        )
        organization_user.save()
        user_profile = UserProfile.objects.create(
            user=organization_user,
        )
        user_profile.organizations.add(organization)


def initialize_administrator(
        username='admin_user@example.com',
        email='admin_user@example.com', password='admin_password'):
    u"""Initialize administrator user.

    :param username: string User username
    :param email: string User email
    :param password: string User plaintext password
    """
    administrator1 = User.objects.create_user(username, email, password)
    administrator1.save()
    administrator_profile = UserProfile.objects.create(user=administrator1)
    administrator_profile.is_administrator = True
    administrator_profile.save()
    return administrator1
