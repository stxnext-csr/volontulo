# -*- coding: utf-8 -*-

u"""
.. module:: setup
"""

import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='volontulo',
    version='alpha',
    packages=['volontulo'],
    include_package_data=True,
    license='MIT License',
    description='Simple Django app connecting organizations with volonteers.',
    long_description=README,
    test_suite='runtests.runtests',
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
