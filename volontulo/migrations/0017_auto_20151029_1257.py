# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0016_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='status_old',
        ),
        migrations.AddField(
            model_name='offer',
            name='status',
            field=models.OneToOneField(related_name='offer', to='volontulo.OfferStatus', null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='time_period',
            field=models.CharField(default='', max_length=150),
        ),
    ]
