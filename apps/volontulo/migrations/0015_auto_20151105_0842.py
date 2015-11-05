# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0014_merge'),
    ]

    operations = [
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
            name='action_status',
            field=models.CharField(max_length=16, default='ongoing', choices=[('future', 'Future'), ('ongoing', 'Ongoing'), ('finished', 'Finished')]),
        ),
        migrations.AddField(
            model_name='offer',
            name='constant_coop',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='offer',
            name='finished_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='offer_status',
            field=models.CharField(max_length=16, default='unpublished', choices=[('unpublished', 'Unpublished'), ('published', 'Published'), ('rejected', 'Rejected')]),
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
            name='recruitment_status',
            field=models.CharField(max_length=16, default='open', choices=[('open', 'Open'), ('supplemental', 'Supplemental'), ('closed', 'Closed')]),
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
            name='started_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='volunteers_limit',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='status_old',
            field=models.CharField(max_length=30, default='NEW', null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='time_period',
            field=models.CharField(max_length=150, default='', blank=True),
        ),
    ]
