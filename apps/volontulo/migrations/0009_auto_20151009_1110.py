# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0008_usergallery_is_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergallery',
            name='image',
            field=models.ImageField(upload_to='profile/'),
        ),
    ]
