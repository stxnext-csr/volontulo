# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0013_auto_20151028_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerstatus',
            name='action_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='offerstatus',
            name='action_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
