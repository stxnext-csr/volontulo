# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('slug', models.CharField(max_length=150)),
                ('priority', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('time_commitment', models.TextField()),
                ('benefits', models.TextField()),
                ('location', models.CharField(max_length=150)),
                ('title', models.CharField(max_length=150)),
                ('time_period', models.CharField(max_length=150)),
                ('status_old', models.CharField(max_length=30, default='NEW')),
                ('votes', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OfferImage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('path', models.ImageField(upload_to='offers/')),
                ('is_main', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('offer', models.ForeignKey(to='volontulo.Offer')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('path', models.ImageField(upload_to='gallery/')),
                ('is_main', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(related_name='images', to='volontulo.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='UserBadges',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('description', models.CharField(max_length=255)),
                ('counter', models.IntegerField(blank=True, default=0)),
                ('badge', models.ForeignKey(to='volontulo.Badge')),
                ('content_type', models.ForeignKey(null=True, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='UserGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('image', models.ImageField(upload_to='profile/')),
                ('is_avatar', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('is_administrator', models.BooleanField(default=False)),
                ('uuid', models.UUIDField(unique=True, default=uuid.uuid4)),
                ('badges', models.ManyToManyField(through='volontulo.UserBadges', to='volontulo.Badge', related_name='user_profile')),
                ('organizations', models.ManyToManyField(to='volontulo.Organization', related_name='userprofiles')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='usergallery',
            name='userprofile',
            field=models.ForeignKey(related_name='images', to='volontulo.UserProfile'),
        ),
        migrations.AddField(
            model_name='userbadges',
            name='userprofile',
            field=models.ForeignKey(db_column='userprofile_id', to='volontulo.UserProfile'),
        ),
        migrations.AddField(
            model_name='organizationgallery',
            name='published_by',
            field=models.ForeignKey(related_name='gallery', to='volontulo.UserProfile'),
        ),
        migrations.AddField(
            model_name='offerimage',
            name='userprofile',
            field=models.ForeignKey(related_name='offerimages', to='volontulo.UserProfile'),
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
