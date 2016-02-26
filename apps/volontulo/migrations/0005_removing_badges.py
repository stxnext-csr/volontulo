# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0004_auto_20151118_1157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbadges',
            name='badge',
        ),
        migrations.RemoveField(
            model_name='userbadges',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='userbadges',
            name='userprofile',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='badges',
        ),
        migrations.DeleteModel(
            name='Badge',
        ),
        migrations.DeleteModel(
            name='UserBadges',
        ),
    ]
