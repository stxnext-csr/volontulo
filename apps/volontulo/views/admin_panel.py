"""
.. module:: admin_panel
"""
from django.shortcuts import render


def main_panel(request):
    """Main admin panel view."""

    return render(
        request,
        'admin/list_offers.html'
    )
