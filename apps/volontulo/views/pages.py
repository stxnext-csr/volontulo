# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView
)
from django.views.generic.list import ListView


from apps.volontulo.models import Page


# pylint: disable=too-many-ancestors,missing-docstring
class PageList(ListView):
    model = Page
    template_name = 'pages/page_list.html'

    @method_decorator(user_passes_test(
            lambda u: u.is_authenticated() and u.userprofile.is_administrator))
    def dispatch(self, *args, **kwargs):
        return super(PageList, self).dispatch(*args, **kwargs)


# pylint: disable=too-many-ancestors,missing-docstring
class PageDetails(DetailView):
    model = Page
    template_name = 'pages/page_detail.html'


# pylint: disable=too-many-ancestors,missing-docstring
class PageCreate(CreateView):
    model = Page
    fields = (
        'title',
        'content',
        'published',
    )
    template_name = 'pages/page_edit_form.html'
    success_url = reverse_lazy('pages_list')

    def form_valid(self, form):
        # pylint: disable=attribute-defined-outside-init
        self.object = form.save(commit=False)
        self.object.author = self.request.user.userprofile
        self.object.save()
        return redirect(self.get_success_url())

    @method_decorator(user_passes_test(
        lambda u: u.is_authenticated() and u.userprofile.is_administrator))
    def dispatch(self, *args, **kwargs):
        return super(PageCreate, self).dispatch(*args, **kwargs)


# pylint: disable=too-many-ancestors,missing-docstring
class PageEdit(UpdateView):
    model = Page
    fields = (
        'title',
        'content',
        'published',
    )
    template_name = 'pages/page_edit_form.html'
    success_url = reverse_lazy('pages_list')

    @method_decorator(user_passes_test(
            lambda u: u.is_authenticated() and u.userprofile.is_administrator))
    def dispatch(self, *args, **kwargs):
        return super(PageEdit, self).dispatch(*args, **kwargs)


# pylint: disable=too-many-ancestors,missing-docstring
class PageDelete(DeleteView):
    model = Page
    success_url = reverse_lazy('pages_list')

    def get(self, request, *args, **kwargs):
        """
        method overrides default get method to, allow deletion
        without confirmation
        """
        return self.post(request, *args, **kwargs)

    @method_decorator(user_passes_test(
        lambda u: u.userprofile.is_administrator and u.is_authenticated()))
    def dispatch(self, *args, **kwargs):
        return super(PageDelete, self).dispatch(*args, **kwargs)
