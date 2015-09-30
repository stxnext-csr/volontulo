# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_badges(apps, schema_editor):
    Badge = apps.get_model('volontulo', 'Badge')
    records = Badge.objects.all().count()
    initial = [
        {
            'name': 'Wolontariusz',
            'slug': 'volunteer',
            'priority': 1,
        },
        {
            'name': 'Uczestnik',
            'slug': 'participant',
            'priority': 2,
        },
        {
            'name': 'Wybitny uczestnik',
            'slug': 'prominent-participant',
            'priority': 3,
        }
    ]
    if records != 3:
        for row in initial:
            Badge(**row).save()


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0005_auto_20150930_1130'),
    ]

    operations = [
        migrations.RunPython(populate_badges),
    ]
