# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_badges(apps, schema_editor):
    Badge = apps.get_model('volontulo', 'Badge')
    records = Badge.objects.all().count()
    initial = [
        {
            'name': u'Wolontariusz',
            'slug': u'volunteer',
            'priority': 1,
        },
        {
            'name': u'Uczestnik',
            'slug': u'participant',
            'priority': 2,
        },
        {
            'name': u'Wybitny uczestnik',
            'slug': u'prominent-participant',
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
