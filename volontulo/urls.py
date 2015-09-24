# -*- coding: utf-8 -*-

u"""
.. module:: urls
"""

from django.conf.urls import url

from volontulo import views
from volontulo.views import offers as offers_views
from volontulo.views import organizations as orgs_views


urlpatterns = [  # pylint: disable=invalid-name
    # homepage:
    url(r'^$', views.index, name='index'),

    # login and loggged user space:
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^me$', views.logged_user_profile, name='logged_user_profile'),
    # password-reset
    # me/edit
    # me/settings

    # offers' namesapce:
    url(r'^offers$', offers_views.offers_list, name='offers_list'),
    url(
        r'^offers/form/(?P<organization_id>[0-9]+)$',
        offers_views.offer_form,
        name='offer_form'
    ),
    url(
        r'^offers/form/(?P<organization_id>[0-9]+)/(?P<offer_id>[0-9]+)$',
        offers_views.offer_form,
        name='offer_form'
    ),
    url(
        r'^offers/activate/(?P<offer_id>[0-9]+)$',
        offers_views.activate_offer,
        name='activate_offer'
    ),
    url(
        r'^offers/(?P<slug>[\w-]+)/(?P<offer_id>[0-9]+)$',
        offers_views.show_offer,
        name='show_offer'
    ),
    url(
        r'^offers/(?P<slug>[\w-]+)/(?P<offer_id>[0-9]+)/join$',
        offers_views.offer_apply,
        name='offer_apply'
    ),
    # offers/filter
    # offers/create

    # users' namesapce:
    # users
    # users/filter
    # users/slug-id
    # users/slug-id/contact

    # organizations' namespace:
    # organizations
    # organizations/filter
    # organization/create
    url(
        r'^organizations/(?P<slug>[\w-]+)/(?P<organization_id>[0-9]+)$',
        orgs_views.organization_view,
        name='organization_view'
    ),
    url(
        r'^organizations/(?P<slug>[\w-]+)/(?P<organization_id>[0-9]+)/edit$',
        orgs_views.organization_form,
        name='organization_form'
    ),
    # organizations/<slug>/<id>/contact

    # others:
    url(
        r'^pages/(?P<template_name>[\w-]+)$',
        views.static_pages,
        name='static_page'
    ),
    url(
        r'^contact$',
        views.contact_form,
        name='contact_form'
    ),
]
