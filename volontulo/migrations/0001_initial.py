# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.CharField(max_length=150)),
                ('priority', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('time_commitment', models.TextField()),
                ('benefits', models.TextField()),
                ('location', models.CharField(max_length=150)),
                ('title', models.CharField(max_length=150)),
                ('time_period', models.CharField(max_length=150)),
                ('status', models.CharField(default='STAGED', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserBadges',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('description', models.CharField(max_length=255)),
                ('badge', models.ForeignKey(to='volontulo.Badge')),
                ('content_type', models.ForeignKey(null=True, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('is_administrator', models.BooleanField(default=False)),
                ('badges', models.ManyToManyField(related_name='user_profile', to='volontulo.Badge', through='volontulo.UserBadges')),
                ('organization', models.ForeignKey(null=True, blank=True, to='volontulo.Organization')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userbadges',
            name='userprofile',
            field=models.ForeignKey(db_column='userprofile_id', to='volontulo.UserProfile'),
        ),
        migrations.AddField(
            model_name='offer',
            name='organization',
            field=models.ForeignKey(to='volontulo.Organization'),
        ),
        migrations.AddField(
            model_name='offer',
            name='volunteers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
