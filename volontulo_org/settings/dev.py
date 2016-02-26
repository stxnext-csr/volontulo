"""
Development Settings Module
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DEBUG_TOOLBAR_PATCH_SETTINGS = False

INSTALLED_APPS += (
    'debug_toolbar',
    'django_coverage',
    'django_extensions',
    'django_nose'
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
