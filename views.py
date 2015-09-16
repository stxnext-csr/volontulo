# -*- coding: utf-8 -*-

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import TemplateDoesNotExist

from . import models
from volontulo.forms import UserForm, CreateOfferForm
from volontulo.forms import ProfileForm
from volontulo.models import UserProfile


def index(request):
    return HttpResponse(u"Welcome in volontulo app.")

def login(request):
    if request.method == 'GET':
        return render(request, "volontulo/login.html")
    username = request.POST['login']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return redirect('user_profile')
        else:
            return HttpResponse(u"Konto zostało wyłączone!")
    else:
        return HttpResponse(u"Nieprawidłowy email lub hasło!")


@login_required
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


def static_pages(request, template_name):
    try:
        return render(
            request,
            "volontulo/static_pages/{}.html".format(template_name)
        )
    except TemplateDoesNotExist:
        raise Http404


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                user = User.objects.get(email=request.POST.get('email'))
            except User.DoesNotExist:
                user = None
            if user:
                messages.add_message(
                    request,
                    messages.INFO,
                    u'Użytkownik o podanym emailu już istnieje'
                )
                return HttpResponseRedirect(reverse('register'))
            else:
                # save user
                user = user_form.save(commit=False)
                user.set_password(request.POST.get('password'))
                # to prevent username UNIQUE constraint
                user.username = user.email
                user.save()
                # save profile
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                send_mail(
                    u'Rejestracja na Wolontulo',
                    u'Dziękujemy za rejestrację.',
                    'support@volontulo.org',
                    [user.email],
                    fail_silently=False
                )
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    u'Rejestracja przebiegła pomyślnie'
                )
                return HttpResponseRedirect(reverse('register'))
        else:
            messages.add_message(
                request,
                messages.ERROR,
                u'Wprowadzono nieprawidłowy email lub hasło'
            )
            return HttpResponseRedirect(reverse('register'))

    user_form = UserForm()
    profile_form = ProfileForm()
    return render(
        request,
        'volontulo/register.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )

@login_required
def create_offer(request):
    # if request.user.is_anonymous():
    #     return redirect('login')

    if request.method == 'POST':
        form = CreateOfferForm(request.POST)
        if form.is_valid():
            offer = form.save()
            send_mail(
                u'Zgłoszenie oferty na Volontulo',
                u'ID oferty: {0}.'.format(offer.id),
                'support@volontulo.org',
                ['filip.gorczynski@gmail.com'], # todo: zmienić na docelowy
                fail_silently=False
            )
            messages.add_message(
                request,
                messages.INFO,
                u"Dziękujemy za dodanie oferty. Aby była widoczna musi zostać zaakceptowana przez moderatora."
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                u"Formularz zawiera niepoprawnie wypełnione pola"
            )
            return render(
                request,
                'volontulo/create_offer.html',
                {
                    'form': form
                }
            )
    form = CreateOfferForm()
    return render(request, 'volontulo/create_offer.html', {'form': form})

@login_required 
def user_profile(request):
    user = get_object_or_404(UserProfile, user__email=request.user)

    return render(
        request,
        'volontulo/user_account.html',
        {
            'user': user
        }
    )
