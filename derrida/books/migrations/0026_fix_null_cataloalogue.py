# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-20 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0025_help_text_catatalogue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogue',
            name='call_number',
            field=models.CharField(blank=True, default='', help_text='Used for Derrida shelf mark', max_length=255),
            preserve_default=False,
        ),
    ]
