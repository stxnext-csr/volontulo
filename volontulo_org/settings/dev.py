"""
Development Settings Module
"""
# pylint: skip-file

from .base import *

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += (
    'debug_toolbar',
    'django_coverage',
    'django_extensions',
    'django_nose'
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
