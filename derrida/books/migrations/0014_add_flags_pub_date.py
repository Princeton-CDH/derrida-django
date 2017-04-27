# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-16 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0013_add_journal_type_item_type_dates'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='pub_day_missing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='book',
            name='pub_month_missing',
            field=models.BooleanField(default=False),
        ),
    ]
