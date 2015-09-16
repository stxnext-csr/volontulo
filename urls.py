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
        r'^organization/view',
        views.organization_view,
        name='organization_view'
    ),
    url(
        r'^organization/form',
        views.organization_form,
        name='organization_form'
    ),
]
