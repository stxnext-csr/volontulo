# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from . import models


def index(request):
    return HttpResponse(u"Welcome in volontulo app.")


def list_offers(request):
    offers = models.Offer.objects.all()
    return render(request, "volontulo/list_offers.html", context={
        'offers': offers,
    })


def show_offer(request, offer_id):
    offer = get_object_or_404(models.Offer, id=offer_id)
    return render(request, "volontulo/show_offer.html", context={
        'offer': offer,
    })
