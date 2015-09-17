# -*- coding: utf-8 -*-

u"""
.. module:: urls
"""

from django.conf.urls import url

from . import views


urlpatterns = [  # pylint: disable=invalid-name
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register, name='register'),
    url(r'^auth/login', views.login, name='login'),
    url(r'^auth/logout', views.logout, name='logout'),
    url(r'^user/profile', views.user_profile, name='user_profile'),
    url(
        r'^page/(?P<template_name>[\w-]+)$',
        views.static_pages,
        name='static_page'
    ),
    url(r'^offers/list$', views.list_offers, name='list_offers'),
    url(
        r'^offers/activate/(?P<offer_id>[0-9]+)$',
        views.activate_offer,
        name='activate_offer'
    ),
    url(
        r'^offers/show/(?P<offer_id>[0-9]+)$',
        views.show_offer,
        name='show_offer'
    ),
    url(
        r'^offers/create$',
        views.create_offer,
        name='create_offer'
    ),
    url(
        r'^organizations/show/(?P<organization_id>[0-9]+)$',
        views.organization_view,
        name='organization_view'
    ),
    url(
        r'^organizations/edit',
        views.organization_form,
        name='organization_form'
    ),
    url(
        r'^offers/apply/(?P<offer_id>[0-9]+)$',
        views.offer_apply,
        name='offer_apply'
    ),
]
