# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-26 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_set_known_language_codes'),
    ]

    operations = [
        migrations.AddField(
            model_name='derridawork',
            name='zotero_id',
            field=models.CharField(blank=True, default='', max_length=8),
        ),
        migrations.AlterField(
            model_name='instance',
            name='zotero_id',
            field=models.CharField(blank=True, default='', max_length=8),
        ),
    ]
