# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0004_userbadges_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='votes',
            field=models.BooleanField(default=0),
        ),
    ]
