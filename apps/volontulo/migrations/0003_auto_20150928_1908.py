# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def move_organization(apps, schema_editor):
    UserProfile = apps.get_model('volontulo', 'UserProfile')
    for up in UserProfile.objects.all():
        if up.organization:
            up.organizations.add(up.organization)


class Migration(migrations.Migration):

    dependencies = [
        ('volontulo', '0002_remove_userprofile_is_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='organizations',
            field=models.ManyToManyField(to='volontulo.Organization'),
        ),
        migrations.RunPython(move_organization),
        migrations.RemoveField(
            model_name='userprofile',
            name='organization',
        ),
    ]
