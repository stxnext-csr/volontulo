# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('volontulo', '0004_auto_20150929_0901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbadges',
            name='user',
        ),
        migrations.AddField(
            model_name='badge',
            name='slug',
            field=models.CharField(max_length=150, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offer',
            name='votes',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='userbadges',
            name='content_type',
            field=models.ForeignKey(null=True, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='userbadges',
            name='counter',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='userbadges',
            name='userprofile',
            field=models.ForeignKey(db_column='userprofile_id', to='volontulo.UserProfile', default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.CharField(max_length=30, default='NEW'),
        ),
    ]
