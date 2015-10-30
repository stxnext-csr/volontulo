# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0005_auto_20150930_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('image', models.FileField(upload_to='profile/')),
                ('userprofile', models.ForeignKey(related_name='images', to='volontulo.UserProfile')),
            ],
        ),
    ]
