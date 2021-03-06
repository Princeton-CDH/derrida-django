# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 19:26
from __future__ import unicode_literals

from django.core.management import call_command
from django.contrib.auth.management import create_permissions
from django.db import migrations


def load_fixture(apps, schema_editor):
    # ensure permissions have been created before loading fixture
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    call_command('loaddata', 'data_editor_group', app_label='common', verbose=0)


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_squashed_0033_remove_book_models'),
        ('people', '0001_initial'),
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=migrations.RunPython.noop),
    ]
