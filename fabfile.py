# -*- coding: utf-8 -*-

u"""
.. module:: fabfile

Be aware, that becaus fabric doesn't support py3k You need to execute this
particular script using Python 2.
"""

import contextlib

from fabric.api import cd
from fabric.api import env
from fabric.api import prefix
from fabric.api import run

env.user = 'root'
env.hosts = ['volontuloapp.org']
env.forward_agent = True


def update():
    u"""Function defining all steps required to properly update application."""

    # Django app refresh:
    with contextlib.nested(
        cd('/var/www/volontuloapp_org/volontulo'),
        prefix('workon volontulo')
    ):
        run('git checkout master')
        run('git pull')
        run('pip install -r requirements.txt')

    # Gulp frontend refresh:
    with contextlib.nested(
        cd('/var/www/volontuloapp_org/volontulo/volontulo')
    ):
        run('npm install .')
        run('./node_modules/gulp/bin/gulp.js build')

    # Django site refresh:
    with contextlib.nested(
        cd('/var/www/volontuloapp_org'),
        prefix('workon volontulo')
    ):
        run('python manage.py migrate --traceback')
        run('service apache2 restart')
