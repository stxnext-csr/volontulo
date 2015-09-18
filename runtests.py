# -*- coding: utf-8 -*-

u"""
.. module:: runtests
"""

import os
import sys

import django
from django.conf import settings
from django.core.management import call_command
from django.test.utils import get_runner


os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'

test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)


def runtests():
    u"""Set up environment and run tests."""
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    django.setup()
    call_command('makemigrations', 'volontulo')
    failures = test_runner.run_tests(['volontulo'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()
