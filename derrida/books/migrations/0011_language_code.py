# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-02 02:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_work_author_optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='code',
            field=models.CharField(blank=True, help_text='two or three letter language code from ISO 639', max_length=3, null=True),
        )
    ]
