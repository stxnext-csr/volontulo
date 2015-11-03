# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0017_auto_20151029_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='status_old',
            field=models.CharField(default='NEW', null=True, max_length=30),
        ),
    ]
