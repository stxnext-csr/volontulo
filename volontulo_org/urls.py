from os import path

from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

PROJECT_ROOT = path.dirname(path.dirname(__file__))

urlpatterns = [
    url(r'^volontulo/', include('apps.volontulo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {
            'document_root': path.join(PROJECT_ROOT, 'static')
        }
    ),
    url(
        r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {
            'document_root': settings.MEDIA_ROOT
        }
    ),
]
