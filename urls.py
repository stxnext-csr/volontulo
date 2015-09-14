# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url('offers/show/(?P<id_>[0-9]+)$', views.show_offer, name='show_offer'),
]
