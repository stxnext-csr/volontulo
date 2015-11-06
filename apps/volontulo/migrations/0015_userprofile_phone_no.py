# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0014_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone_no',
            field=models.CharField(max_length=32, default='', blank=True, null=True),
        ),
    ]
