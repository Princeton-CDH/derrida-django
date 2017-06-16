# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 19:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djiffy', '0001_initial'),
        ('books', '0001_squashed_0033_remove_book_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='digital_edition',
            field=models.ForeignKey(blank=True, help_text='Digitized edition of this book, if available', null=True, on_delete=django.db.models.deletion.CASCADE, to='djiffy.Manifest'),
        ),
    ]