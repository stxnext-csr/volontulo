# -*- coding: utf-8 -*-
u"""
.. module:: addbadges
"""
from django.core.management.base import BaseCommand

from apps.volontulo.models import Badge


class Command(BaseCommand):
    u"""Badge management CLI."""
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        u"""Handle CLI tool for creating badges.

        :param args:
        :param options:
        :return:
        """
        badges = Badge.objects.all().count()
        self.stdout.write('Current badges number: %d' % badges)
        # pylint: disable=bad-builtin
        confirm = input("Do you want to reset badges? [yes/NO] ")
        if confirm == 'yes':
            self.stdout.write("Removing badges from database.")
            Badge.objects.all().delete()
            initial = [
                {
                    'name': u'Wolontariusz',
                    'slug': 'volunteer',
                    'priority': 1,
                },
                {
                    'name': u'Uczestnik',
                    'slug': 'participant',
                    'priority': 2,
                },
                {
                    'name': u'Wybitny uczestnik',
                    'slug': 'prominent-participant',
                    'priority': 3,
                },
            ]
            for badge in initial:
                Badge.objects.create(
                    name=badge.get('name'),
                    slug=badge.get('slug'),
                    priority=badge.get('priority'),
                )
                self.stdout.write('Badge "%s" added' % badge.get('name'))
        else:
            self.stdout.write("Removing badges cancelled.")
