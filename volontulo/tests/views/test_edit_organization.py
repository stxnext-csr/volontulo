# -*- coding: utf-8 -*-

u"""
.. module:: test_edit_organization
"""
from volontulo.tests.views.test_organizations import TestOrganizations


class TestEditOrganization(TestOrganizations):
    u"""Class responsible for testing editing organization specific views."""

    # # pylint: disable=invalid-name
    # def test__edit_organization_get_form_anonymous(self):
    #     u"""Get organization edit form as anonymous."""
    #     response = self.client.get(
    #         '/organizations/organization-1/1/edit',
    #         follow=True,
    #     )
    #
    #     self.assertRedirects(
    #         response,
    #         '/organizations/organization-1/1/edit',
    #         302,
    #         200,
    #     )
    #     self.assertEqual(len(response.redirect_chain), 1)
    #     self.assertEqual(
    #         response.redirect_chain[0],
    #         (
    #             '/organizations/organization-1/1/edit',
    #             302
    #         ),
    #     )
    #
    # # pylint: disable=invalid-name
    # def test__edit_organization_post_form_anonymous(self):
    #     u"""Post organization edit form as anonymous."""
    #     response = self.client.post(
    #         '/organizations/organization-1/1/edit',
    #         follow=True,
    #     )
    #
    #     self.assertRedirects(
    #         response,
    #         'http://testserver/login?'
    #         'next=/organizations/organization-1/1/edit',
    #         302,
    #         200,
    #     )
    #     self.assertEqual(len(response.redirect_chain), 1)
    #     self.assertEqual(
    #         response.redirect_chain[0],
    #         (
    #             'http://testserver/login?'
    #             'next=/organizations/organization-1/1/edit',
    #             302
    #         ),
    #     )
    #
    # # pylint: disable=invalid-name
    # def test__edit_organization_get_form_volunteer(self):
    #     u"""Get organization edit form as volunteer."""
    #     self.client.post('/login', {
    #         'email': u'volunteer1@example.com',
    #         'password': 'volunteer1',
    #     })
    #     response = self.client.get(
    #         '/organizations/organization-1/1/edit',
    #         follow=True,
    #     )
    #
    #     self.assertRedirects(
    #         response,
    #         '/organizations/organization-1/1',
    #         302,
    #         200,
    #     )
    #     self.assertEqual(len(response.redirect_chain), 1)
    #     self.assertEqual(
    #         response.redirect_chain[0],
    #         (
    #             '/organizations/organization-1/1',
    #             302
    #         ),
    #     )
    #     self.assertContains(
    #         response,
    #         u'Nie masz uprawnień do edycji tej organizacji.'
    #     )
    #
    # # pylint: disable=invalid-name
    # def test__edit_organization_post_form_volunteer(self):
    #     u"""Post organization edit form as volunteer."""
    #     self.client.post('/login', {
    #         'email': u'volunteer1@example.com',
    #         'password': 'volunteer1',
    #     })
    #     response = self.client.post(
    #         '/organizations/organization-1/1/edit',
    #         follow=True,
    #     )
    #
    #     self.assertRedirects(
    #         response,
    #         '/organizations/organization-1/1',
    #         302,
    #         200,
    #     )
    #     self.assertEqual(len(response.redirect_chain), 1)
    #     self.assertEqual(
    #         response.redirect_chain[0],
    #         (
    #             '/organizations/organization-1/1',
    #             302
    #         ),
    #     )
    #     self.assertContains(
    #         response,
    #         u'Nie masz uprawnień do edycji tej organizacji.'
    #     )
    #
    # # pylint: disable=invalid-name
    # def test__edit_organization_get_form_other_organization(self):
    #     u"""Get organization edit form as other organization."""
    #     self.client.post('/login', {
    #         'email': u'organization2@example.com',
    #         'password': 'organization2',
    #     })
    #     response = self.client.get(
    #         '/organizations/organization-1/1/edit',
    #         follow=True,
    #     )
    #
    #     self.assertRedirects(
    #         response,
    #         '/organizations/organization-1/1',
    #         302,
    #         200,
    #     )
    #     self.assertEqual(len(response.redirect_chain), 1)
    #     self.assertEqual(
    #         response.redirect_chain[0],
    #         (
    #             '/organizations/organization-1/1',
    #             302
    #         ),
    #     )
    #     self.assertContains(
    #         response,
    #         u'Nie masz uprawnień do edycji tej organizacji.'
    #     )
    #
    # # pylint: disable=invalid-name
    # def test__edit_organization_post_form_other_organization(self):
    #     u"""Post organization edit form as other organization."""
    #     self.client.post('/login', {
    #         'email': u'organization2@example.com',
    #         'password': 'organization2',
    #     })
    #     response = self.client.post(
    #         '/organizations/organization-1/1/edit',
    #         follow=True,
    #     )
    #
    #     self.assertRedirects(
    #         response,
    #         '/organizations/organization-1/1',
    #         302,
    #         200,
    #     )
    #     self.assertEqual(len(response.redirect_chain), 1)
    #     self.assertEqual(
    #         response.redirect_chain[0],
    #         (
    #             '/organizations/organization-1/1',
    #             302
    #         ),
    #     )
    #     self.assertContains(
    #         response,
    #         u'Nie masz uprawnień do edycji tej organizacji.'
    #     )
    #
    # # pylint: disable=invalid-name
    # def test__edit_organization_get_form_right_organization(self):
    #     u"""Get organization edit form as right organization."""
    #     self.client.post('/login', {
    #         'email': u'organization1@example.com',
    #         'password': 'organization1',
    #     })
    #     response = self.client.get(
    #         '/organizations/organization-1/1/edit',
    #         follow=True,
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, u'Nazwa')
    #     self.assertContains(response, u'Adres')
    #     self.assertContains(response, u'Opis')
    #     # pylint: disable=no-member
    #     self.assertIn('organization', response.context)
    #
    # # pylint: disable=invalid-name
    # def test__edit_organization_post_form_right_organization(self):
    #     u"""Post organization edit form as right organization."""
    #     self.client.post('/login', {
    #         'email': u'organization1@example.com',
    #         'password': 'organization1',
    #     })
    #     form_params = {}
    #     response = self.client.post(
    #         '/organizations/organization-1/1/edit',
    #         form_params,
    #         follow=True,
    #     )
    #
    #     self.assertRedirects(
    #         response,
    #         '/organizations/organization-1/1',
    #         302,
    #         200,
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, u'Oferta została dodana/zmieniona.')
