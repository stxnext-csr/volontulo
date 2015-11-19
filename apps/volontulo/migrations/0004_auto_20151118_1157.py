# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0003_offer_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='requirements',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='offerimage',
            name='offer',
            field=models.ForeignKey(to='volontulo.Offer', related_name='images'),
        ),
    ]
