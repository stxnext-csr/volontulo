# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone_no',
            field=models.CharField(blank=True, null=True, max_length=32, default=''),
        ),
    ]
