# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-01-11 10:18
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DevilryReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('started_datetime', models.DateTimeField(blank=True, default=None, null=True)),
                ('finished_datetime', models.DateTimeField(blank=True, default=None, null=True)),
                ('generator_type', models.CharField(max_length=255)),
                ('generator_options', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('status', models.CharField(choices=[(b'unprocessed', b'unprocessed'), (b'generating', b'generating'), (b'success', b'success'), (b'error', b'error')], default=b'unprocessed', max_length=255)),
                ('status_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('output_filename', models.CharField(blank=True, default=b'', max_length=255, null=True)),
                ('result', models.BinaryField()),
                ('generated_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
