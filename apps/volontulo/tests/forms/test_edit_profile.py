# -*- coding: utf-8 -*-

u"""
.. module:: test_edit_profile
"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TransactionTestCase

from apps.volontulo.forms import EditProfileForm
from apps.volontulo.tests import common


class TestEditProfileForm(TransactionTestCase):
    u"""Tests for register view."""

    def setUp(self):
        u"""UnitTest setup data."""
        common.initialize_empty_volunteer()

    def test_is_validate_passed_passwords_form_is_valid(self):
        u"""Test is_validate() method.

            Testing EditProfileForm.is_valid() method
            with correct passwords and other fields
            return valid form
        """
        form_data = dict(
            email='volunteer1@example.com',
            current_password='volunteer1',
            new_password='new_valid_password',
            confirm_new_password='new_valid_password',
            user=User.objects.get(email='volunteer1@example.com').id,
        )
        form = EditProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test__is_validate__empty_passwords__form_is_not_valid(self):
        u"""Test is_validate() method.

            Testing EditProfileForm.is_valid() method
            with empty passwords and other fields
            return not valid form
        """
        form_data = dict()
        form = EditProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test__is_validate__wrong_current_password__raise_exception(self):
        u"""Test is_validate() method.

            Testing EditProfileForm.is_valid() method
            with incorrect current password
            raise ValidationError exception
        """
        form_data = dict(
            email='volunteer1@example.com',
            current_password='xxx',
            new_password='new_valid_password',
            confirm_new_password='new_valid_password',
            user=User.objects.get(email='volunteer1@example.com').id,
        )
        form = EditProfileForm(data=form_data)
        self.assertRaises(ValidationError, form.is_valid)

    def test__is_validate__distinct_new_passwords__raise_exception(self):
        u"""Test is_validate() method.

            Testing EditProfileForm.is_valid() method
            with distinct new passwords
            raise ValidationError exception
        """
        form_data = dict(
            email='volunteer1@example.com',
            current_password='xxx',
            new_password='new_valid_password',
            confirm_new_password='new_valid_password',
            user=User.objects.get(email='volunteer1@example.com').id,
        )
        form = EditProfileForm(data=form_data)
        self.assertRaises(ValidationError, form.is_valid)

    def test__no_is_avatar_field_on_edit_profile_form(self):
        u"""Test if Is Avatar field is not visible."""

        self.client.post('/login', {
            'email': u'volunteer1@example.com',
            'password': 'volunteer1',
        })
        response = self.client.get('/me')
        self.assertNotContains(response, u'is_avatar')
