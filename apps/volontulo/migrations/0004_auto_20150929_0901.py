# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0003_auto_20150928_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='organizations',
            field=models.ManyToManyField(related_name='userprofiles', to='volontulo.Organization'),
        ),
    ]
