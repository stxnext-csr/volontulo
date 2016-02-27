# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView
)
from django.views.generic.list import ListView


from apps.volontulo.models import Page


# pylint: disable=too-many-ancestors;missing-docstring
class PageList(ListView):
    model = Page
    template_name = 'pages/page_list.html'


# pylint: disable=too-many-ancestors;missing-docstring
class PageDetails(DetailView):
    model = Page
    template_name = 'pages/page_detail.html'


# pylint: disable=too-many-ancestors;missing-docstring
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


# pylint: disable=too-many-ancestors;missing-docstring
class PageEdit(UpdateView):
    model = Page
    fields = (
        'title',
        'content',
        'published',
    )
    template_name = 'pages/page_edit_form.html'
    success_url = reverse_lazy('pages_list')


# pylint: disable=too-many-ancestors;missing-docstring
class PageDelete(DeleteView):
    model = Page
    success_url = reverse_lazy('pages_list')

    def get(self, request, *args, **kwargs):
        """
        method overrides default get method to, allow deletion
        without confirmation
        """
        return self.post(request, *args, **kwargs)
