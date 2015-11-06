# -*- coding: utf-8 -*-

u"""
.. module:: test_settings_sqlite

The application uses PosgreSQL database. However, to run the test slightly
faster you may use SQLite to run them locally using this settings file.
Don't forget to run the tests on the production RDBMS before pushing your
changes (test_settings module).
"""
# pylint: skip-file

from .test_settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
