# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-13 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_reference_canvases'),
        ('interventions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='interventions',
            field=models.ManyToManyField(blank=True, to='interventions.Intervention'),
        ),
    ]
