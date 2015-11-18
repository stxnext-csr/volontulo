# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_null_weight_rows(apps, schema_editor):
    Offer = apps.get_model('volontulo', 'Offer')
    records = Offer.objects.filter(weight__isnull=True)
    for row in records:
        row.weight = 0
        Offer(**row).save()

class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0002_userprofile_phone_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='weight',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.RunPython(populate_null_weight_rows),
    ]
