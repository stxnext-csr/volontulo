# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0019_auto_20151030_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerstatus',
            name='action_ongoing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='offerstatus',
            name='constant_coop',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='offerstatus',
            name='reserve_recruitment',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='offerstatus',
            name='reserve_recruitment_end_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='offerstatus',
            name='reserve_recruitment_start_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
