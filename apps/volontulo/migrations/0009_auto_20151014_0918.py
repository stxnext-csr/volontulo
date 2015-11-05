# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.db import migrations, models


def populate_uuid_fields(apps, schema_editor):
    UserProfile = apps.get_model('volontulo', 'UserProfile')
    # clean whole column prevently
    UserProfile.objects.all().update(uuid='')
    for item in UserProfile.objects.all():
        if not item.uuid:
            item.uuid = str(uuid.uuid4()).replace('-', '') #creates a random GUID
            item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0008_userprofile_uuid'),
    ]

    operations = [
        migrations.RunPython(populate_uuid_fields),
        migrations.AlterField(
            model_name='userprofile',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, blank=True),
        ),
    ]
