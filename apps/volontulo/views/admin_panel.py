"""
.. module:: admin_panel
"""
from django.shortcuts import render


def main_panel(request):

    return render(
        request,
        'admin/list_offers.html'
    )
