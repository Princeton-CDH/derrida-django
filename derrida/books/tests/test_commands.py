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
    reference_data


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

        assert self.importer.import_manifest(manifest_uri, path) is None
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
