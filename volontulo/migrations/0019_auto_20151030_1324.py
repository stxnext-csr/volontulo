# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0018_offer_status_old'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='time_period',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='offerstatus',
            name='volunteers_limit',
            field=models.IntegerField(null=True, blank=True, default=0),
        ),
    ]
