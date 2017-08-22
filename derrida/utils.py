'''
Utilities for Derrida

1) Code for safely loading fixtures based on their historical serializer not their
current one. Adapted almost verbatim from
https://stackoverflow.com/questions/32912112/django-loaddata-in-migrations-errors

2) Cleanup function to remove Latin ligatures and replace with 'ae' and 'oe'
'''
import os

from io import StringIO

import django.apps

from django.conf import settings
from django.core import serializers
from django.core.management import call_command
from django.db import connection


os.environ['DJANGO_COLORS'] = 'nocolor'


def reset_sqlsequence(apps=None, schema_editor=None):
    """Suitable for use in migrations.RunPython and used to set Postgres
    SQL sequence, making migrations database agnostic
    See https://stackoverflow.com/a/44337543
    """

    commands = StringIO()
    cursor = connection.cursor()
    patched = False

    if apps:
        # Monkey patch django.apps
        original_apps = django.apps.apps
        django.apps.apps = apps
        patched = True
    else:
        # If not in a migration, use the normal apps registry
        apps = django.apps.apps

    for app in apps.get_app_configs():
        # Generate the sequence reset queries
        label = app.label
        if patched and app.models_module is None:
            # Defeat strange test in the mangement command
            app.models_module = True
        call_command('sqlsequencereset', label, stdout=commands)
        if patched and app.models_module is True:
            app.models_module = None

    if patched:
        # Cleanup monkey patch
        django.apps.apps = original_apps

    sql = commands.getvalue()
    print(sql)
    if sql:
        # avoid DB error if sql is empty
        cursor.execute(commands.getvalue())


class LoadFixtureData(object):
    '''Fixture loader that uses the state of the serializer at the time of the
    migration, NOT the current one. Necessary for any models that have later
    changes and pre-loaded fixtures'''
    def __init__(self, *files):
        '''        
        :param files: args style list of fixture files
        :type list:
        '''
        self.files = files

    def __call__(self, apps=None, schema_editor=None):
        if apps:
            # if in a migration Monkey patch the app registry
            # this avoids the use of the wrong serializer
            original_apps = serializers.python.apps
            serializers.python.apps = apps

        for fixture_file in self.files:
            with open(fixture_file) as fixture:
                objects = serializers.deserialize('json', fixture)

                for obj in objects:
                    obj.save()

        if apps:
            # Cleanup monkey patch
            serializers.python.apps = original_apps


def deligature(value):
    '''Remove common unicode characters Œ and Æ plus lowercase equivalents.'''
    mapping = {
        u'\u00C6': 'Ae',
        u'\u0152': 'Oe',
        u'\u00E6': 'ae',
        u'\u0153': 'oe'
    }

    return value.translate(str.maketrans(mapping))
