# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0012_organizationgallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('offer_status', models.CharField(choices=[('unpublished', 'Unpublished'), ('published', 'Published'), ('rejected', 'Rejected')], max_length=16)),
                ('recruitment_status', models.CharField(choices=[('open', 'Open'), ('supplemental', 'Supplemental'), ('closed', 'Closed')], max_length=16)),
                ('action_status', models.CharField(choices=[('future', 'Future'), ('ongoing', 'Ongoing'), ('finished', 'Finished')], max_length=16)),
            ],
        ),
        migrations.RemoveField(
            model_name='offer',
            name='time_period',
        ),
        migrations.AddField(
            model_name='offer',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 13, 7, 8, 149005, tzinfo=utc), auto_now_add=True),
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
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 10, 28, 13, 7, 17, 100429, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.OneToOneField(related_name='offer', to='volontulo.OfferStatus'),
        ),
    ]
