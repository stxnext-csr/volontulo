# -*- coding: utf-8 -*-


from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from . import models


def index(request):
    return HttpResponse(u"Welcome in volontulo app.")


def login(request):
    if request.method == 'GET':
        return render(request, "volontulo/login.html")
    username = request.POST['login']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    auth.login(request, user)
    return HttpResponse(u"it's login.")


def logout(request):
    auth.logout(request)
    return HttpResponse(u"it's logout.")


def list_offers(request):
    if (
        request.user.is_authenticated() and
        models.UserProfile.objects.get(user=request.user).is_admin
    ):
        offers = models.Offer.objects.all()
    else:
        offers = models.Offer.objects.filter(status='ACTIVE')
    return render(request, "volontulo/list_offers.html", context={
        'offers': offers,
    })


def activate_offer(request, offer_id):
    offer = get_object_or_404(models.Offer, id=offer_id)
    offer.status = 'ACTIVE'
    offer.save()
    return redirect('list_offers')


def show_offer(request, offer_id):
    offer = get_object_or_404(models.Offer, id=offer_id)
    return render(request, "volontulo/show_offer.html", context={
        'offer': offer,
    })
