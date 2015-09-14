# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url('offers/list', views.list_offers, name='list_offers'),
    url('offers/show/(?P<offer_id>[0-9]+)$', views.show_offer, name='show_offer'),
]
