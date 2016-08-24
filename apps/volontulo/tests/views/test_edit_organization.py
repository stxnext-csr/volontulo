# -*- coding: utf-8 -*-

u"""
.. module:: test_edit_organization
"""
from apps.volontulo.tests.views.test_organizations import TestOrganizations


class TestEditOrganization(TestOrganizations):
    u"""Class responsible for testing editing organization specific views."""

    def test__edit_organization_get_form_anonymous(self):
        u"""Get organization edit form as anonymous."""
        response = self.client.get(
            '/organizations/organization-1/{}/edit'.format(
                self.organization.id),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            'http://testserver/login?'
            'next=/organizations/organization-1/{}/edit'.format(
                self.organization.id),
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            (
                'http://testserver/login?'
                'next=/organizations/organization-1/{}/edit'.format(
                    self.organization.id
                ),
                302
            ),
        )

    def test__edit_organization_post_form_anonymous(self):
        u"""Post organization edit form as anonymous."""
        response = self.client.get(
            '/organizations/organization-1/{}/edit'.format(
                self.organization.id),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            'http://testserver/login?'
            'next=/organizations/organization-1/{}/edit'.format(
                self.organization.id),
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            (
                'http://testserver/login?'
                'next=/organizations/organization-1/{}/edit'.format(
                    self.organization.id
                ),
                302
            ),
        )

    def test__edit_organization_get_form_volunteer(self):
        u"""Get organization edit form as volunteer."""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get(
            '/organizations/organization-1/{}/edit'.format(
                self.organization.id
            ),
            follow=True,
        )

        self.assertRedirects(
            response,
            '/organizations/organization-1/{}'.format(self.organization.id),
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            (
                'http://testserver/organizations/organization-1/{}'.format(
                    self.organization.id
                ),
                302
            ),
        )
        self.assertContains(
            response,
            u'Nie masz uprawnień do edycji tej organizacji.'
        )

    def test__edit_organization_post_form_volunteer(self):
        u"""Post organization edit form as volunteer."""
        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get(
            '/organizations/organization-1/{}/edit'.format(
                self.organization.id
            ),
            follow=True,
        )

        self.assertRedirects(
            response,
            '/organizations/organization-1/{}'.format(self.organization.id),
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            (
                'http://testserver/organizations/organization-1/{}'.format(
                    self.organization.id
                ),
                302
            ),
        )
        self.assertContains(
            response,
            u'Nie masz uprawnień do edycji tej organizacji.'
        )

    def test__edit_organization_get_form_other_organization(self):
        u"""Get organization edit form as other organization."""
        self.client.post('/login', {
            'email': u'organization2@example.com',
            'password': 'organization2',
        })
        response = self.client.get(
            '/organizations/organization-1/{}/edit'.format(
                self.organization.id
            ),
            follow=True,
        )

        self.assertRedirects(
            response,
            '/organizations/organization-1/{}'.format(self.organization.id),
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            (
                'http://testserver/organizations/organization-1/{}'.format(
                    self.organization.id
                ),
                302
            ),
        )
        self.assertContains(
            response,
            u'Nie masz uprawnień do edycji tej organizacji.'
        )

    def test__edit_organization_post_form_other_organization(self):
        u"""Post organization edit form as other organization."""
        self.client.post('/login', {
            'email': u'organization2@example.com',
            'password': 'organization2',
        })
        response = self.client.get(
            '/organizations/organization-1/{}/edit'.format(
                self.organization.id),
            follow=True,
        )

        self.assertRedirects(
            response,
            '/organizations/organization-1/{}'.format(self.organization.id),
            302,
            200,
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(
            response.redirect_chain[0],
            (
                'http://testserver/organizations/organization-1/{}'.format(
                    self.organization.id
                ),
                302
            ),
        )
        self.assertContains(
            response,
            u'Nie masz uprawnień do edycji tej organizacji.'
        )

    def test__edit_organization_get_form_right_organization(self):
        u"""Get organization edit form as right organization."""
        self.client.post('/login', {
            'email': u'organization1@example.com',
            'password': 'organization1',
        })
        response = self.client.get(
            '/organizations/organization-1/{}/edit'.format(
                self.organization.id
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('organization', response.context)
        self.assertContains(response, u'Nazwa')
        self.assertContains(response, u'Adres')
        self.assertContains(response, u'Opis')
        self.assertContains(response, u'Zapisz zmiany')
        self.assertEqual(
            response.context['organization'].name,
            u'Organization 1'
        )
        self.assertEqual(
            response.context['organization'].address,
            u'Organization 1 address'
        )
        self.assertEqual(
            response.context['organization'].description,
            u'Organization 1 description'
        )

    def test__edit_organization_post_form_right_organization(self):
        u"""Post organization edit form as right organization."""
        self.client.post('/login', {
            'email': u'organization1@example.com',
            'password': 'organization1',
        })
        # not enough data send
        form_params = {
            'name': u'',
            'address': u'',
            'description': u'',
        }
        response = self.client.post(
            '/organizations/organization-1/{}/edit'.format(
                self.organization.id),
            form_params,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            u"Należy wypełnić wszystkie pola formularza."
        )

        # properly filled form
        form_params = {
            'name': u'New Organization 1 name',
            'address': u'New Organization 1 address',
            'description': u'New Organization 1 description',
        }

        response = self.client.post(
            '/organizations/organization-1/{}/edit'.format(
                self.organization.id
            ),
            form_params,
            follow=True,
        )

        self.assertRedirects(
            response,
            '/organizations/new-organization-1-name/{}'.format(
                self.organization.id
            ),
            302,
            200,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u'Oferta została dodana/zmieniona.')
