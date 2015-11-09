# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0011_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationGallery',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('path', models.ImageField(upload_to='gallery/')),
                ('is_main', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(related_name='images', to='volontulo.Organization')),
                ('published_by', models.ForeignKey(related_name='gallery', to='volontulo.UserProfile')),
            ],
        ),
    ]
