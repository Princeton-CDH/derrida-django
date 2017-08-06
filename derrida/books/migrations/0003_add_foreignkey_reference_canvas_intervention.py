# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-03 19:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interventions', '0001_initial'),
        ('djiffy', '0002_view_permissions'),
        ('books', '0002_connect_book_references_canvases_manifests'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='canvases',
            field=models.ManyToManyField(blank=True, help_text="Scanned images from Derrida's Library | ", to='djiffy.Canvas'),
        ),
        migrations.AddField(
            model_name='reference',
            name='interventions',
            field=models.ManyToManyField(blank=True, to='interventions.Intervention'),
        ),
    ]