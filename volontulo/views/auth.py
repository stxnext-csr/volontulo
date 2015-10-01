# -*- coding: utf-8 -*-

u"""
.. module:: auth
"""

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render

from volontulo.forms import ProfileForm
from volontulo.forms import UserForm
from volontulo.lib.email import FROM_ADDRESS
from volontulo.lib.email import send_mail


def login(request):
    u"""Login view."""
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    u"Poprawnie zalogowano"
                )

            else:
                messages.add_message(
                    request,
                    messages.INFO,
                    u"Konto zostało wyłączone!"
                )
        else:
            messages.add_message(
                request,
                messages.ERROR,
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


def register(request):
    u"""View responsible for registering new users."""
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                user = User.objects.get(email=request.POST.get('email'))
            except User.DoesNotExist:
                user = None
            if user:
                messages.add_message(
                    request,
                    messages.INFO,
                    u'Użytkownik o podanym emailu już istnieje'
                )
                return redirect('register')
            else:
                # save user
                user = user_form.save(commit=False)
                user.set_password(request.POST.get('password'))
                # to prevent username UNIQUE constraint
                user.username = user.email
                user.save()
                # save profile
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                send_mail('registration', [user.email])
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    u'Rejestracja przebiegła pomyślnie'
                )
                return redirect('register')
        else:
            messages.add_message(
                request,
                messages.ERROR,
                u'Wprowadzono nieprawidłowy email lub hasło'
            )
            return redirect('register')

    user_form = UserForm()
    profile_form = ProfileForm()
    return render(
        request,
        'auth/register.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )


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
