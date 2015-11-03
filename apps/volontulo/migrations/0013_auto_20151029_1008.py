# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0012_organizationgallery'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offer',
            old_name='status',
            new_name='status_old',
        ),
    ]
