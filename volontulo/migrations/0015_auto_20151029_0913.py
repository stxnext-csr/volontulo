# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0014_auto_20151028_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerstatus',
            name='recruitment_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='offerstatus',
            name='recruitment_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='offerstatus',
            name='volunteers_limit',
            field=models.IntegerField(default=0),
        ),
    ]
