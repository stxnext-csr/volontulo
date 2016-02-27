# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0006_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='slug',
        ),
    ]
