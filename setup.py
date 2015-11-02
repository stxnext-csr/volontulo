# -*- coding: utf-8 -*-

u"""
.. module:: setup
"""

import os
from distutils.command.install import install
from setuptools import setup
from subprocess import check_output

REPO_ROOT = os.path.dirname(__file__)


class install_with_gulp(install):
    u"""Class extending install command - responsible for building fronted."""

    def run(self):
        u"""Definition of custom install command."""
        check_output(
            ['npm', 'install', '--quiet'],
            cwd=os.path.join(REPO_ROOT, 'volontulo'),
        )
        check_output(
            ['gulp', 'build'],
            cwd=os.path.join(REPO_ROOT, 'volontulo')
        )
        install.run(self)

with open(os.path.join(REPO_ROOT, 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='volontulo',
    version='alpha',
    packages=['apps.volontulo'],
    include_package_data=True,
    license='MIT License',
    description='Simple Django app connecting organizations with volonteers.',
    long_description=README,
    cmdclass=dict(install=install_with_gulp),
    url='http://volontuloapp.org/',
    author='Tomasz Magulski',
    author_email='tomasz.magulski@stxnext.pl',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
