# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('priority', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserBadges',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('description', models.CharField(max_length=255)),
                ('badge', models.ForeignKey(to='volontulo.Badge')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_organization', models.BooleanField(default=False)),
                ('is_administrator', models.BooleanField(default=False)),
                ('badges', models.ManyToManyField(related_name='user_profile', to='volontulo.Badge', through='volontulo.UserBadges')),
                ('organization', models.ForeignKey(to='volontulo.Organization', blank=True, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userbadges',
            name='user',
            field=models.ForeignKey(to='volontulo.UserProfile'),
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
