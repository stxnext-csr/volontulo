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

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'fake_emails')
