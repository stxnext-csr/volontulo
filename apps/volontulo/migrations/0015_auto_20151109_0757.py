# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0014_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('offer_status', models.CharField(choices=[('unpublished', 'Unpublished'), ('published', 'Published'), ('rejected', 'Rejected')], max_length=16)),
                ('recruitment_status', models.CharField(choices=[('open', 'Open'), ('supplemental', 'Supplemental'), ('closed', 'Closed')], max_length=16)),
                ('recruitment_start_date', models.DateTimeField(blank=True, null=True)),
                ('recruitment_end_date', models.DateTimeField(blank=True, null=True)),
                ('action_status', models.CharField(choices=[('future', 'Future'), ('ongoing', 'Ongoing'), ('finished', 'Finished')], max_length=16)),
                ('action_start_date', models.DateTimeField(blank=True, null=True)),
                ('action_end_date', models.DateTimeField(blank=True, null=True)),
                ('volunteers_limit', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='offer',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 7, 57, 22, 259293, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offer',
            name='finished_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 7, 57, 27, 227012, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='offer',
            name='status_old',
            field=models.CharField(default='NEW', null=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='offer',
            name='time_period',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='offer',
            name='status',
            field=models.OneToOneField(related_name='offer', to='volontulo.OfferStatus', null=True),
        ),
    ]
