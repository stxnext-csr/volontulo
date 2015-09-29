# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0003_auto_20150929_0544'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbadges',
            name='counter',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
