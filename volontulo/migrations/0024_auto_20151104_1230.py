# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0023_auto_20151104_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='finished_at',
            field=models.DateTimeField(null=True, default='', blank=True),
        ),
    ]
