# -*- coding: utf-8 -*-

u"""
.. module:: auth
"""

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import View

from volontulo.forms import UserForm
from volontulo.lib.email import FROM_ADDRESS
from volontulo.lib.email import send_mail
from volontulo.models import UserProfile
from volontulo.utils import yield_message_error
from volontulo.utils import yield_message_successful


def login(request):
    u"""Login view."""
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                yield_message_successful(
                    request,
                    u"Poprawnie zalogowano"
                )
            else:
                messages.add_message(
                    request,
                    messages.INFO,
                    u"Konto zostało wyłączone!"
                )
        else:
            yield_message_error(
                request,
                u"Nieprawidłowy email lub hasło!"
            )
        return redirect('homepage')
    else:
        return render(
            request,
            'auth/login.html',
            {}
        )


@login_required
def logout(request):
    u"""Logout view."""
    auth.logout(request)
    messages.add_message(
        request,
        messages.INFO,
        u"Użytkownik został wylogowany!"
    )
    return redirect('homepage')


class Register(View):
    u"""View responsible for registering new users."""

    @staticmethod
    def get(request):
        u"""Simple view to render register form."""
        return render(
            request,
            'auth/register.html',
            {
                'user_form': UserForm(),
            }
        )

    @staticmethod
    def post(request):
        u"""Method handes creation of new user."""
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            try:
                user = User.objects.create_user(
                    username=request.POST.get('email'),
                    email=request.POST.get('email'),
                    password=request.POST.get('password'),
                )
            except IntegrityError:
                messages.add_message(
                    request,
                    messages.INFO,
                    u'Użytkownik o podanym emailu już istnieje'
                )
                return redirect('register')
            else:
                profile = UserProfile(user=user)
                profile.save()

                send_mail(request, 'registration', [user.email])
                yield_message_successful(
                    request,
                    u'Rejestracja przebiegła pomyślnie'
                )
                return redirect('register')
        else:
            yield_message_error(
                request,
                u'Wprowadzono nieprawidłowy email lub hasło'
            )
            return redirect('register')


def password_reset(request):
    u"""View responsible for password reset."""
    return auth_views.password_reset(
        request,
        template_name='auth/password_reset.html',
        post_reset_redirect='login',
        from_email=FROM_ADDRESS,
        subject_template_name='emails/password_reset.subject',
        email_template_name='emails/password_reset.txt',
        html_email_template_name='emails/password_reset.html',
    )


def password_reset_confirm(request, uidb64, token):
    u"""Landing page for password reset."""
    return auth_views.password_reset_confirm(
        request,
        uidb64,
        token,
        template_name='auth/password_reset_confirm.html',
        post_reset_redirect='login',
    )
