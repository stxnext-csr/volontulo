# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0021_auto_20151103_0911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='status',
        ),
        migrations.AddField(
            model_name='offer',
            name='action_status',
            field=models.CharField(choices=[('future', 'Future'), ('ongoing', 'Ongoing'), ('finished', 'Finished')], default='ongoing', max_length=16),
        ),
        migrations.AddField(
            model_name='offer',
            name='offer_status',
            field=models.CharField(choices=[('unpublished', 'Unpublished'), ('published', 'Published'), ('rejected', 'Rejected')], default='unpublished', max_length=16),
        ),
        migrations.AddField(
            model_name='offer',
            name='recruitment_status',
            field=models.CharField(choices=[('open', 'Open'), ('supplemental', 'Supplemental'), ('closed', 'Closed')], default='open', max_length=16),
        ),
        migrations.DeleteModel(
            name='OfferStatus',
        ),
    ]
