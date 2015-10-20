# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0007_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergallery',
            name='is_avatar',
            field=models.BooleanField(default=False),
        ),
    ]
