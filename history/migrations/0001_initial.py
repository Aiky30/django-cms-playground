# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-18 13:21
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='FIL_History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('page_data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('placeholders', django.contrib.postgres.fields.jsonb.JSONField()),
                ('plugins', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_history', to='cms.Page')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title_history', to='cms.Title')),
            ],
        ),
    ]
