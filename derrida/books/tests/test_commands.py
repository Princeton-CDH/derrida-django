from io import StringIO
from unittest.mock import MagicMock, patch

from django.core.management.base import CommandError
from django.db.models import QuerySet
from django.test import TestCase, override_settings
from djiffy.models import Manifest
from pytest import raises

from derrida.books.management.commands import export_zotero, import_digitaleds
from derrida.books.models import DerridaWork, Instance


class TestManifestImporter(TestCase):
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
        short_id = '123ab'
        db_manif = Manifest(label='Test Manifest', short_id=short_id)
        # NOTE: using unsaved db manifest object to avoid import skipping
        # due to manifest uri already being in the database
        mocksuperimport.return_value = db_manif
        assert self.importer.import_manifest(manifest_uri, path) == db_manif
        mockerror_msg.assert_called_with('No finding aid URL found for %s' % \
            short_id)

        # findingaid url but no match for an instance in the db
        fa_url = "http://findingaids.princeton.edu/collections/RBD1/c9156"
        db_manif.extra_data = {
            fa_url: {}
        }
        self.importer.import_manifest(manifest_uri, path)
        mockerror_msg.assert_called_with('No matching instance for %s (%s)' % \
            (short_id, fa_url))

        # finding aid url matches instance in the db fixture
        fa_url = "http://findingaids.princeton.edu/collections/RBD1/c9157"
        db_manif.extra_data = {
            fa_url: {}
        }
        # must be saved in the db to link to book record
        db_manif.save()
        self.importer.import_manifest(manifest_uri, path)
        inst = Instance.objects.get(uri=fa_url)
        assert inst.digital_edition == db_manif


@patch('derrida.books.management.commands.import_digitaleds.DerridaManifestImporter')
class TestImportDigitalEds(TestCase):

    def setUp(self):
        self.cmd = import_digitaleds.Command()
        self.cmd.stdout = StringIO()

    def test_command(self, mockimporter):
        # normal file/uri
        test_paths = ['one', 'two']
        self.cmd.handle(path=test_paths, update=False)
        assert mockimporter.return_value.import_paths.called_with(test_paths)

        # shortcut for PUL derrida collection
        self.cmd.handle(path=['PUL'], update=False)
        assert mockimporter.return_value.import_paths \
            .called_with([self.cmd.manifest_uris['PUL']])

        # works within a list also
        self.cmd.handle(path=['one', 'PUL', 'two'], update=False)
        assert mockimporter.return_value.import_paths \
            .called_with(['one', self.cmd.manifest_uris['PUL'], 'two'])

    def test_summarize(self, mockimporter):
        # 3 urls processed nothing done
        self.cmd.summarize({'urls': 3, 'manifests': 0})
        output = self.cmd.stdout.getvalue()
        assert 'URLs processed: 3' in output
        # imports/errors not reported if there are none
        assert 'Manifests' not in output
        assert 'not matched' not in output

        self.cmd.summarize({'urls': 3, 'manifests': 1, 'nomatch': 0})
        output = self.cmd.stdout.getvalue()
        assert 'Manifests imported or updated: 1' in output
        # import/error not reported if there are none
        assert 'not matched' not in output

        # report no matches
        self.cmd.summarize({'urls': 3, 'manifests': 2, 'nomatch': 1})
        output = self.cmd.stdout.getvalue()
        assert 'Manifests not matched to library work instances: 1' in output

@patch('pyzotero.zotero.Zotero')
@override_settings(ZOTERO_API_KEY='foo', ZOTERO_LIBRARY_ID='bar')
class TestExportZotero(TestCase):
    fixtures = ['sample_work_data.json']
    
    def setUp(self):
        self.cmd = export_zotero.Command()
        self.cmd.stdout = StringIO()

    def test_handle(self, zotero):
        self.cmd.create_collections = MagicMock()
        self.cmd.create_items = MagicMock()
        # API key is required
        with self.settings(ZOTERO_API_KEY=None):
            with raises(CommandError):
                self.cmd.handle()
                output = self.cmd.stdout.getvalue()
                assert 'API key must be set' in output
        # Zotero library ID is required
        with self.settings(ZOTERO_API_KEY='foo', ZOTERO_LIBRARY_ID=None):
            with raises(CommandError):
                self.cmd.handle()
                output = self.cmd.stdout.getvalue()
                assert 'library ID must be set' in output
        # Should initialize a library with provided values
        self.cmd.handle()
        assert zotero.called_once_with(('foo', 'group', 'bar'))
        # Should call create_collections with new works
        dlg = DerridaWork.objects.get(pk=1) # no zotero id ("new")
        assert self.cmd.create_collections.called_once_with(QuerySet(dlg))
        # Should call create_items with all cited instances
        assert self.cmd.create_items.called_once_with(Instance.objects.all())
    
    def test_create_collections(self, zotero):
        # Should report if nothing in queryset
        self.cmd.create_collections(DerridaWork.objects.none())
        output = self.cmd.stdout.getvalue()
        assert 'No collections' in output
        # Should output how many new works were provided
        self.cmd.library = MagicMock()
        self.cmd.create_collections(DerridaWork.objects.all())
        output = self.cmd.stdout.getvalue()
        assert 'Found 2 new Derrida works' in output
        # Should call create_collections with new work data
        # Should save returned zotero IDs to the works

    @override_settings(ZOTERO_API_KEY='foo', ZOTERO_LIBRARY_ID='bar')
    def test_create_items(self, zotero):
        # Should report if nothing in queryset
        # Should output how many instances were provided
        # Should convert instances to zotero items
        # Should call create_items with the item data
        # Should save returned zotero IDs to the instances
        # Should output run statistics
        pass