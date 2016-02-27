# -*- coding: utf-8 -*-

u"""
.. module:: urls
"""

from django.conf.urls import url

from apps.volontulo import views
from apps.volontulo.views import auth as auth_views
from apps.volontulo.views import admin_panel as admin_views
from apps.volontulo.views import offers as offers_views
from apps.volontulo.views import organizations as orgs_views
from apps.volontulo.views import pages as pages_views

# pylint: disable=invalid-name
handler404 = 'apps.volontulo.views.page_not_found'
handler500 = 'apps.volontulo.views.server_error'


urlpatterns = [  # pylint: disable=invalid-name
    # homepage:
    url(r'^$', views.homepage, name='homepage'),

    # login and loggged user space:
    url(r'^login$', auth_views.login, name='login'),
    url(r'^logout$', auth_views.logout, name='logout'),
    url(r'^register$', auth_views.Register.as_view(), name='register'),
    url(
        r'^activate/(?P<uuid>[-0-9A-Za-z]+)$',
        auth_views.activate,
        name='activate'
    ),
    url(r'^password-reset$', auth_views.password_reset, name='password_reset'),
    url(
        r'^password-reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'
    ),
    url(r'^me$', views.logged_user_profile, name='logged_user_profile'),
    # me/edit
    # me/settings

    # offers' namesapce:
    url(r'^offers$', offers_views.OffersList.as_view(), name='offers_list'),
    url(
        r'^offers/delete/(?P<pk>[0-9]+)$',
        offers_views.OffersDelete.as_view(),
        name='offers_delete'
    ),
    url(
        r'^offers/accept/(?P<pk>[0-9]+)$',
        offers_views.OffersAccept.as_view(),
        name='offers_accept'
    ),
    url(
        r'^offers/create$',
        offers_views.OffersCreate.as_view(),
        name='offers_create'
    ),
    url(
        r'^offers/reorder/(?P<id_>[0-9]+)?$',
        offers_views.OffersReorder.as_view(),
        name='offers_reorder'
    ),
    url(
        r'^offers/archived$',
        offers_views.OffersArchived.as_view(),
        name='offers_archived'
    ),
    url(
        r'^offers/(?P<slug>[\w-]+)/(?P<id_>[0-9]+)$',
        offers_views.OffersView.as_view(),
        name='offers_view'
    ),
    url(
        r'^offers/(?P<slug>[\w-]+)/(?P<id_>[0-9]+)/edit$',
        offers_views.OffersEdit.as_view(),
        name='offers_edit'
    ),
    url(
        r'^offers/(?P<slug>[\w-]+)/(?P<id_>[0-9]+)/join$',
        offers_views.OffersJoin.as_view(),
        name='offers_join'
    ),
    # offers/filter

    # users' namesapce:
    # users
    # users/filter
    # users/slug-id
    # users/slug-id/contact

    # organizations' namespace:
    url(
        r'^organizations$',
        orgs_views.organizations_list,
        name='organizations_list'
    ),
    url(
        r'^organizations/create$',
        orgs_views.OrganizationsCreate.as_view(),
        name='organizations_create',
    ),
    url(
        r'^organizations/(?P<slug>[\w-]+)/(?P<id_>[0-9]+)$',
        orgs_views.organization_view,
        name='organization_view'
    ),
    url(
        r'^organizations/(?P<slug>[\w-]+)/(?P<id_>[0-9]+)/edit$',
        orgs_views.organization_form,
        name='organization_form'
    ),
    # organizations/filter
    # organizations/<slug>/<id>/contact


    # pages:
    url(
        r'^pages$',
        pages_views.PageList.as_view(),
        name='pages_list'
    ),
    url(
        r'^pages/create$',
        pages_views.PageCreate.as_view(),
        name='pages_create'
    ),
    url(
        r'^pages/(?P<pk>[0-9]+)/edit',
        pages_views.PageEdit.as_view(),
        name='pages_edit'
    ),
    url(
        r'^pages/(?P<pk>[0-9]+)/delete',
        pages_views.PageDelete.as_view(),
        name='pages_delete'
    ),
    url(
        r'^(?P<slug>[-\w]+),(?P<pk>[0-9]+).html$',
        pages_views.PageDetails.as_view(),
        name='pages_detail'
    ),

    # others:
    url(
        r'^o-nas$',
        views.static_pages,
        kwargs={'template_name': 'about-us'},
        name='about-us'
    ),
    url(
        r'^office$',
        views.static_pages,
        kwargs={'template_name': 'office'},
        name='office'
    ),
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
    url(
        r'^panel$',
        admin_views.main_panel,
        name='admin_panel'
    ),
    url(
        r'^newsletter$',
        views.newsletter_signup,
        name='newsletter_signup'
    ),
]
