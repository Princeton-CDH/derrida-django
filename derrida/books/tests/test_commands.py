import codecs
from collections import defaultdict
import csv
from io import StringIO
import json
import os.path
import tempfile
from unittest.mock import Mock, MagicMock, patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.models import QuerySet
from django.test import TestCase, override_settings
from djiffy.models import Manifest
from pytest import raises

from derrida.books.models import Instance, Reference, DerridaWork
from derrida.books.management.commands import import_digitaleds, \
    reference_data, export_zotero


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
@override_settings(ZOTERO_API_KEY='z_apikey', ZOTERO_LIBRARY_ID='z_group')
class TestExportZotero(TestCase):
    fixtures = ['sample_work_data.json']

    def setUp(self):
        self.cmd = export_zotero.Command()
        self.cmd.stdout = StringIO()

    def test_handle(self, zotero):
        with patch.object(self.cmd, 'create_collections') as mock_create_collections:
            with patch.object(self.cmd, 'create_items') as mock_create_items:

                mock_create_items.return_value = {'created': 0, 'updated': 0,
                    'unchanged': 0, 'failed': 0}

                # API key is required
                with self.settings(ZOTERO_API_KEY=None):
                    with raises(CommandError):
                        self.cmd.handle()
                        output = self.cmd.stdout.getvalue()
                        assert 'API key must be set' in output

                        mock_create_collections.assert_not_called()
                        mock_create_items.assert_not_called()

                # Zotero library ID is required
                with self.settings(ZOTERO_LIBRARY_ID=None):
                    with raises(CommandError):
                        self.cmd.handle()
                        output = self.cmd.stdout.getvalue()
                        assert 'library ID must be set' in output

                # Should initialize a library with provided values
                self.cmd.handle()
                assert zotero.called_once_with(('z_apikey', 'group', 'z_group'))
                # Should call create_collections with new works
                dlg = DerridaWork.objects.get(pk=1) # no zotero id ("new")
                assert self.cmd.create_collections.called_once_with(QuerySet(dlg))
                # Should call create_items with all cited instances
                assert self.cmd.create_items.called_once_with(Instance.objects.all())

    def test_create_collections(self, zotero):
        # Should report if nothing in queryset
        # not in verbose mode; should not report anything
        self.cmd.create_collections(DerridaWork.objects.none())
        output = self.cmd.stdout.getvalue()
        assert not output

        # should report nothing to do when verbosity is higher
        self.cmd.verbosity = 2
        self.cmd.create_collections(DerridaWork.objects.none())
        output = self.cmd.stdout.getvalue()
        assert 'No collections' in output

        # Should output how many new works were provided
        self.cmd.library = Mock()
        zotero_id = '12345'
        zotero_id2 = '67890'
        # zotero returns a dict
        self.cmd.library.create_collections.return_value = {
            'success': {'0': zotero_id, '1': zotero_id2}
        }
        self.cmd.create_collections(DerridaWork.objects.all())
        output = self.cmd.stdout.getvalue()
        assert 'Found 2 new Derrida works' in output

        derridaworks = DerridaWork.objects.all()

        # Should call create_collections with new work data
        args = self.cmd.library.create_collections.call_args[0]
        # first arg should be the list of collection names
        for dwork in derridaworks:
            assert {'name': dwork.short_title} in args[0]
        # Should save returned zotero IDs in the database
        assert derridaworks[0].zotero_id == zotero_id
        assert derridaworks[1].zotero_id == zotero_id2

    @patch.object(Instance, 'as_zotero_item')
    def test_create_items(self, mock_as_zotero_item, zotero):
        # use mock for zotero library instance
        self.cmd.library = Mock()
        self.cmd.library.count_items.side_effect = [0, 3]
        self.cmd.library.last_modified_version.return_value = 'Tuesday'
        zotero_response = {
            'success': {
                '0': 'abc',
                '1': 'def',
                '2': 'ghi'
            },
            'unchanged': {},
            'failed': {}
        }
        self.cmd.library.create_items.return_value = zotero_response

        # Should report if no items to report
        # not in verbose mode; should not report anything
        self.cmd.create_items(Instance.objects.none())
        output = self.cmd.stdout.getvalue()
        assert not output

        # should report nothing to do when verbosity is higher
        self.cmd.verbosity = 2
        self.cmd.create_items(Instance.objects.none())
        output = self.cmd.stdout.getvalue()
        assert 'No items to create' in output

        # test with three records
        test_instances = Instance.objects.all()[:3]

        # Should output how many instances were provided
        stats = self.cmd.create_items(test_instances)
        output = self.cmd.stdout.getvalue()
        assert 'Exporting {} instances.'.format(test_instances.count()) in output
        # Should convert instances to zotero items
        # convert to zotero called once per item
        assert mock_as_zotero_item.call_count == test_instances.count()
        mock_as_zotero_item.assert_called_with(self.cmd.library)
        # Should call create_items with the item data
        self.cmd.library.create_items.assert_called_with(
            [mock_as_zotero_item.return_value for i in range(3)],
            last_modified='Tuesday')
        # Should return summary statistics
        assert stats['updated'] == 3
        assert stats['created'] == 3
        assert stats['unchanged'] == 0
        assert stats['failed'] == 0

        # Should save returned zotero IDs to the instances
        for index, inst in enumerate(test_instances):
            assert Instance.objects.get(pk=inst.pk).zotero_id == \
                zotero_response['success'][str(index)]




class TestReferenceData(TestCase):
    fixtures = ['test_references']

    def setUp(self):
        self.cmd = reference_data.Command()
        self.cmd.stdout = StringIO()

    def test_flatten_dict(self):
        # flat dict should not be changed
        flat = {'one': 'a', 'two': 'b'}
        assert flat == self.cmd.flatten_dict(flat)

        # list should be converted to string
        listed = {'one': ['a', 'b']}
        flat_listed = self.cmd.flatten_dict(listed)
        assert flat_listed['one'] == 'a;b'

        # nested dict should have keys combined and be flatted
        nested = {
            'page': {
                'id': 'p1',
                'label': 'one'
            }
        }
        flat_nested = self.cmd.flatten_dict(nested)
        assert 'page id' in flat_nested
        assert 'page label' in flat_nested
        assert flat_nested['page id'] == nested['page']['id']
        assert flat_nested['page label'] == nested['page']['label']

    def test_reference_data(self):
        # reference with no corresponding intervention
        ref = Reference.objects.filter(interventions__isnull=True).first()
        refdata = self.cmd.reference_data(ref)
        assert refdata['id'] == ref.get_uri()
        assert refdata['page'] == ref.derridawork_page
        assert refdata['page location'] == ref.derridawork_pageloc
        assert refdata['book']['id'] == ref.instance.get_uri()
        assert refdata['book']['title'] == ref.instance.display_title()
        assert refdata['book']['page'] == ref.book_page
        assert refdata['type'] == str(ref.reference_type)
        assert refdata['anchor text'] == ref.anchor_text
        assert not refdata['interventions']

        # reference *with* corresponding intervention
        ref = Reference.objects.filter(interventions__isnull=False).first()
        refdata = self.cmd.reference_data(ref)
        # should be referenced by uri
        for intervention in ref.interventions.all():
            assert intervention.get_uri() in refdata['interventions']

    def test_command_line(self):
        # test calling via command line with args

        # generate output in a temporary directory
        with tempfile.TemporaryDirectory(prefix='derrida-refs-') as outputdir:
            stdout = StringIO()
            call_command('reference_data', directory=outputdir, stdout=stdout)

            derrida_work = DerridaWork.objects.first()
            references = Reference.objects.filter(derridawork__id=derrida_work.id)

            base_filename = os.path.join(outputdir,
                                         '%s_references' % derrida_work.slug)

            # inspect JSON output
            with open('{}.json'.format(base_filename)) as jsonfile:
                jsondata = json.load(jsonfile)
                # should be one entry for each reference
                assert len(jsondata) == references.count()
                # spot check the data included
                assert jsondata[0]['id'] == references[0].get_uri()
                assert jsondata[0]['page'] == references[0].derridawork_page
                assert jsondata[0]['page location'] == references[0].derridawork_pageloc
                assert jsondata[3]['page'] == references[3].derridawork_page
                assert jsondata[3]['page location'] == references[3].derridawork_pageloc

            # inspect CSV output
            with open('{}.csv'.format(base_filename)) as csvfile:
                # first byte should be UTF-8 byte order mark
                assert csvfile.read(1) == codecs.BOM_UTF8.decode()

                # then read as CSV
                csvreader = csv.reader(csvfile)

                rows = [row for row in csvreader]
                # row count should be number of refs + header
                assert len(rows) == references.count() + 1
                assert rows[0] == self.cmd.csv_fields
                # spot check the data
                assert str(references[0].derridawork_page) in rows[1]
                assert references[0].derridawork_pageloc in rows[1]
                assert references[0].instance.display_title() in rows[1]
                assert str(references[0].book_page) in rows[1]
                assert references[0].anchor_text in rows[1]
                assert str(references[0].reference_type) in rows[1]
