# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0020_auto_20151103_0724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offerstatus',
            name='action_end_date',
        ),
        migrations.RemoveField(
            model_name='offerstatus',
            name='action_ongoing',
        ),
        migrations.RemoveField(
            model_name='offerstatus',
            name='action_start_date',
        ),
        migrations.RemoveField(
            model_name='offerstatus',
            name='constant_coop',
        ),
        migrations.RemoveField(
            model_name='offerstatus',
            name='recruitment_end_date',
        ),
        migrations.RemoveField(
            model_name='offerstatus',
            name='recruitment_start_date',
        ),
        migrations.RemoveField(
            model_name='offerstatus',
            name='reserve_recruitment',
        ),
        migrations.RemoveField(
            model_name='offerstatus',
            name='reserve_recruitment_end_date',
        ),
        migrations.RemoveField(
            model_name='offerstatus',
            name='reserve_recruitment_start_date',
        ),
        migrations.RemoveField(
            model_name='offerstatus',
            name='volunteers_limit',
        ),
        migrations.AddField(
            model_name='offer',
            name='action_end_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='action_ongoing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='offer',
            name='action_start_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='constant_coop',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='offer',
            name='recruitment_end_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='recruitment_start_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='reserve_recruitment',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='reserve_recruitment_end_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='reserve_recruitment_start_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='volunteers_limit',
            field=models.IntegerField(default=0, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='finished_at',
            field=models.DateTimeField(default='', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='started_at',
            field=models.DateTimeField(default='', blank=True, null=True),
        ),
    ]
