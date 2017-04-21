import json
import os
import requests
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from .viaf import ViafAPI
from rdflib import Graph
from .models import Person, Relationship, RelationshipType, Residence
from derrida.places.models import Place
try:
    # django 1.10
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

# Get the fixtures dir for this app
FIXTURES_PATH = os.path.join(settings.BASE_DIR, 'derrida/people/fixtures')

class TestPerson(TestCase):
    def setUp(self):
        """Load the sample XML file and pass to the TestCase object"""
        fixture_file = os.path.join(FIXTURES_PATH, 'sample_viaf_rdf.xml')
        with open(fixture_file, 'r') as fixture:
            self.mock_rdf = fixture.read()

    def test_str(self):
        pers = Person(authorized_name='Mr. So and So')
        assert str(pers) == 'Mr. So and So'

    def test_dates(self):
        pers = Person.objects.create(authorized_name='Mr. So', birth=1800,
            death=1845)
        # alias fields and actual date range fields should both be set
        assert pers.birth == 1800
        assert pers.start_year == 1800
        assert pers.death == 1845
        assert pers.end_year == 1845

        # queryset filters on alias fields should also work
        assert Person.objects.get(birth=1800) == pers

    @patch('derrida.people.viaf.ViafAPI.get_RDF',
        return_value=Graph().serialize())
    @patch('derrida.people.viaf.ViafAPI.get_years', return_value=(1800, 1900))
    def test_viaf_dates(self, fakedrdf, fakedyears):
        '''Check that if a viaf_id is set, save method will call ViafAPI'''
        pers = Person.objects.create(authorized_name='Mr. X',
            viaf_id='http://notviaf/viaf/0000/')
        assert pers.birth == 1800
        assert pers.death == 1900

class TestResidence(TestCase):

    def setUp(self):
        # test model instances to work with in tests
        self.person = Person(authorized_name='Mrs. W')
        self.place = Place(name='Podunk', geonames_id='7890')
        self.res = Residence(person=self.person, place=self.place)

    def test_str(self):
        # without date
        assert '%s %s' % (self.person, self.place) == str(self.res)
        # include date if there is one
        self.res.start_year = 1900
        assert '%s %s (%s)' % (self.person, self.place, self.res.dates)


class TestRelationshipType(TestCase):

    def test_str(self):
        rel_type = RelationshipType(name='parent')
        assert str(rel_type) == 'parent'


class TestRelationship(TestCase):

    def setUp(self):
        '''Build a test relationship for use'''
        father = Person(authorized_name='Joe Schmoe')
        son = Person(authorized_name='Joe Schmoe Jr.')
        parent = RelationshipType(name='parent')

        father.save()
        son.save()
        parent.save()

        rel = Relationship(from_person=father, to_person=son,
            relationship_type=parent)
        rel.save()

    def test_str(self):
        rel = Relationship.objects.get(pk=1)
        assert str(rel) == 'Joe Schmoe parent Joe Schmoe Jr.'

    def test_through_relationships(self):
        '''Make sure from/to sets make sense and follow consistent naming'''
        father = Person.objects.get(authorized_name='Joe Schmoe')
        son = Person.objects.get(authorized_name='Joe Schmoe Jr.')

        # Not reciprocal, so from_relationships but not to_relationships
        query = father.from_relationships.all()
        assert isinstance(query[0], Relationship)
        assert query[0].from_person == father
        assert query[0].to_person == son

        query = father.to_relationships.all()
        assert not query

        # Check non-reciprocity, from and to person are same for the
        # Relationship object
        query = son.to_relationships.all()
        assert isinstance(query[0], Relationship)
        assert query[0].from_person == father
        assert query[0].to_person == son

        query = son.from_relationships.all()
        assert not query



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


class TestPersonAutocomplete(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username='test',
            password='secret',
            email='foo@bar.com'
        )
        person = Person.objects.create(
            authorized_name='Mr. Author'
        )

    def test_view_behavior(self):
        # No login for anonymous user
        response = self.client.get(reverse('books:publisher-autocomplete'))
        assert response.status_code == 302

        # Get a response as a staff user
        self.client.login(username='test', password='secret')
        response = self.client.get(
            reverse('people:person-autocomplete'),
            params = {'q': 'Mr.'}
        )
        assert response.status_code == 200
        data = json.loads(response.content.decode('utf-8'))
        assert 'results' in data
        assert data['results'][0]['text'] == 'Mr. Author'
        person = Person.objects.get(authorized_name='Mr. Author')
        assert data['results'][0]['id'] == person.id
