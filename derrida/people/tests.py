import os
import requests
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from .viaf import ViafAPI
from rdflib import Graph

# Get the fixtures path for this app
# Get the fixtures dir for this app
FIXTURES_PATH = os.path.join(settings.BASE_DIR, 'derrida/people/fixtures')


class TestViafAPI(TestCase):

    def setUp(self):
        """Load the sample XML file and pass to the TestCase object"""
        fixture_file = os.path.join(FIXTURES_PATH, 'sample_viaf_rdf.xml')
        with open(fixture_file, 'r') as fixture:
            self.mock_rdf = fixture.read()

        graph = Graph()
        self.empty_rdf = graph.serialize()

    @patch('derrida.people.viaf.requests')
    def test_suggest(self, mockrequests):
        viaf = ViafAPI()
        mockrequests.codes = requests.codes
        # Check that query with no matches still returns an empty list
        mock_result = {'query': 'notanauthor', 'result': None}
        mockrequests.get.return_value.status_code = requests.codes.ok
        mockrequests.get.return_value.json.return_value = mock_result
        assert viaf.suggest('notanauthor') == []
        mockrequests.get.assert_called_with(
            'https://www.viaf.org/viaf/AutoSuggest',
            params={'query': 'notanauthor'})

        # valid (abbreviated) response
        mock_result['result'] = [{
          "term": "Austen, Jane, 1775-1817",
          "displayForm": "Austen, Jane, 1775-1817",
          "recordID": "102333412"
        }]
        mockrequests.get.return_value.json.return_value = mock_result
        assert viaf.suggest('austen') == mock_result['result']

        # bad status code on the response - should still return an empty list
        mockrequests.get.return_value.status_code = requests.codes.forbidden
        assert viaf.suggest('test') == []

    def test_get_uri(self):
        assert ViafAPI.uri_from_id('1234') == \
            'https://viaf.org/viaf/1234/'
        # numeric id should also work
        assert ViafAPI.uri_from_id(1234) == \
            'https://viaf.org/viaf/1234/'

    @patch('derrida.people.viaf.requests')
    def test_getRDF(self, mockrequests):
        viaf = ViafAPI()
        mock_rdf = self.mock_rdf
        empty_rdf = self.empty_rdf
        mockrequests.codes = requests.codes

        # Mock a GET that works correctly
        mockrequests.get.return_value.status_code = requests.codes.ok
        mockrequests.get.return_value.text = mock_rdf
        assert viaf.get_RDF('89599270') == mock_rdf

        # Mock a GET that returns a bad code
        mockrequests.get.return_value.status_code = requests.codes.bad
        assert viaf.get_RDF('89599270') == empty_rdf

    def test_get_years(self):
        viaf = ViafAPI()
        mock_rdf = self.mock_rdf
        empty_rdf = self.empty_rdf

        # Test fixture should produce a tuple as follows
        assert viaf.get_years(mock_rdf) == (69, 140)
        # An empty RDF should produce (None, None)
        assert viaf.get_years(empty_rdf) == (None, None)
