# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import uuid
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('slug', models.CharField(max_length=150)),
                ('priority', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('time_commitment', models.TextField()),
                ('benefits', models.TextField()),
                ('location', models.CharField(max_length=150)),
                ('title', models.CharField(max_length=150)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('time_period', models.CharField(blank=True, max_length=150, default='')),
                ('status_old', models.CharField(null=True, max_length=30, default='NEW')),
                ('offer_status', models.CharField(max_length=16, choices=[('unpublished', 'Unpublished'), ('published', 'Published'), ('rejected', 'Rejected')], default='unpublished')),
                ('recruitment_status', models.CharField(max_length=16, choices=[('open', 'Open'), ('supplemental', 'Supplemental'), ('closed', 'Closed')], default='open')),
                ('action_status', models.CharField(max_length=16, choices=[('future', 'Future'), ('ongoing', 'Ongoing'), ('finished', 'Finished')], default='ongoing')),
                ('votes', models.BooleanField(default=0)),
                ('recruitment_start_date', models.DateTimeField(blank=True, null=True)),
                ('recruitment_end_date', models.DateTimeField(blank=True, null=True)),
                ('reserve_recruitment', models.BooleanField(default=True)),
                ('reserve_recruitment_start_date', models.DateTimeField(blank=True, null=True)),
                ('reserve_recruitment_end_date', models.DateTimeField(blank=True, null=True)),
                ('action_ongoing', models.BooleanField(default=False)),
                ('constant_coop', models.BooleanField(default=False)),
                ('action_start_date', models.DateTimeField(blank=True, null=True)),
                ('action_end_date', models.DateTimeField(blank=True, null=True)),
                ('volunteers_limit', models.IntegerField(blank=True, null=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OfferImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('path', models.ImageField(upload_to='offers/')),
                ('is_main', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('offer', models.ForeignKey(to='volontulo.Offer')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('path', models.ImageField(upload_to='gallery/')),
                ('is_main', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(related_name='images', to='volontulo.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='UserBadges',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='profile/')),
                ('is_avatar', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('is_administrator', models.BooleanField(default=False)),
                ('uuid', models.UUIDField(unique=True, default=uuid.uuid4)),
                ('badges', models.ManyToManyField(through='volontulo.UserBadges', related_name='user_profile', to='volontulo.Badge')),
                ('organizations', models.ManyToManyField(related_name='userprofiles', to='volontulo.Organization')),
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
