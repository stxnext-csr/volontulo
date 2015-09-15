# -*- coding: utf-8 -*-

u"""
.. module:: urls
"""

from django.conf.urls import url

from . import views

urlpatterns = [  # pylint: disable=invalid-name
    url('^$', views.index, name='index'),
    url('^auth/login', views.login, name='login'),
    url('^auth/logout', views.logout, name='logout'),
    url(
        r'^page/(?P<template_name>[\w-]+)$',
        views.static_pages,
        name='static_page'
    ),
    url('^offers/list$', views.list_offers, name='list_offers'),
    url(
        '^offers/activate/(?P<offer_id>[0-9]+)$',
        views.activate_offer,
        name='activate_offer'
    ),
    url(
        '^offers/show/(?P<offer_id>[0-9]+)$',
        views.show_offer,
        name='show_offer'
    ),
]
