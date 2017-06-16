# -*- coding: utf-8 -*-
from collections import defaultdict
import os
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from djiffy.models import Manifest

# Common models between projects and associated new types
from derrida.books.models import Instance
from derrida.books.management.commands import import_digitaleds


FIXTURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '..', 'fixtures')


class TestDerridaManifestImporter(TestCase):
    fixtures = ['sample_work_data.json']

    def setUp(self):
        self.importer = import_digitaleds.DerridaManifestImporter()

    @patch('derrida.books.management.commands.import_digitaleds.ManifestImporter.import_manifest')
    @patch('derrida.books.management.commands.import_digitaleds.ManifestImporter.error_msg')
    def test_matching(self, mockerror_msg, mocksuperimport):
        manifest_uri = 'http://so.me/manifest/uri'
        path = '/path/to/manifest.json'

        # simulate import failed
        mocksuperimport.return_value = None

        assert self.importer.import_manifest(manifest_uri, path) == None
        mocksuperimport.assert_called_with(manifest_uri, path)

        # simulate import success but not local identifier
        db_manif = Manifest(label='Test Manifest', short_id='123ab')
        # NOTE: using unsaved db manifest object to avoid import skipping
        # due to manifest uri already being in the database
        mocksuperimport.return_value = db_manif
        assert self.importer.import_manifest(manifest_uri, path) == db_manif
        mockerror_msg.assert_called_with('No source metadata identifier found')

        # local identifier but no match in local book db
        db_manif.metadata = {'Source metadata identifier': ['RBD1.1_c478']}
        self.importer.import_manifest(manifest_uri, path)
        mockerror_msg.assert_called_with('No matching instance for RBD1.1_c478')

        # local identifier matches book in fixture
        db_manif.metadata['Source metadata identifier'] = ['RBD1.c9157']
        # must be saved in the db to link to instance record
        db_manif.save()
        self.importer.import_manifest(manifest_uri, path)
        item = Instance.objects.get(uri='http://findingaids.princeton.edu/collections/RBD1/c9157')
        assert item.digital_edition == db_manif


@patch('derrida.books.management.commands.import_digitaleds.DerridaManifestImporter')
class TestImportDigitalEds(TestCase):

    def test_command(self, mockimporter):
        cmd = import_digitaleds.Command()

        # normal file/uri
        test_paths = ['one', 'two']
        cmd.handle(path=test_paths)
        assert mockimporter.return_value.import_paths.called_with(test_paths)

        # shortcut for nysl
        cmd.handle(path=['PUL'])
        assert mockimporter.return_value.import_paths \
            .called_with([cmd.manifest_uris['PUL']])

        # works within a list also
        cmd.handle(path=['one', 'PUL', 'two'])
        assert mockimporter.return_value.import_paths \
            .called_with(['one', cmd.manifest_uris['PUL'], 'two'])
