# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

from . import models


def index(request):
    return HttpResponse(u"Welcome in volontulo app.")


def show_offer(request, id_):
    offer = models.Offer.objects.get(id=id_)
    return render(request, "volontulo/show_offer.html", context={
        'offer': offer,
    })
