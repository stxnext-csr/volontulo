# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from . import models


def index(request):
    return HttpResponse(u"Welcome in volontulo app.")


def show_offer(request, offer_id):
    offer = get_object_or_404(models.Offer, id=offer_id)
    return render(request, "volontulo/show_offer.html", context={
        'offer': offer,
    })
