# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-13 15:12
from __future__ import unicode_literals

import derrida.interventions.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_allow_neg_years_bc'),
        ('interventions', '0005_intervention_view_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='intervention',
            name='author',
            field=models.ForeignKey(blank=True, default=derrida.interventions.models.get_default_intervener, null=True, on_delete=django.db.models.deletion.CASCADE, to='people.Person'),
        ),
    ]
