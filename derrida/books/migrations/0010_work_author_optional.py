# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-28 00:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_migrate_plum_to_figgy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='authors',
            field=models.ManyToManyField(blank=True, to='people.Person'),
        ),
    ]