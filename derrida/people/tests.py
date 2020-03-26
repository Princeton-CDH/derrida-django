import json
import os
from unittest.mock import patch
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rdflib import Graph
from viapy.api import ViafEntity

from .models import Person, Relationship, RelationshipType, Residence
from derrida.places.models import Place


# fixtures dir for this app
FIXTURES_PATH = os.path.join(settings.BASE_DIR, 'derrida', 'people', 'fixtures')


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

    def test_viaf(self):
        pers = Person(authorized_name='Humperdinck')
        assert pers.viaf is None
        pers.viaf_id = 'http://viaf.org/viaf/35247539'
        assert isinstance(pers.viaf, ViafEntity)
        assert pers.viaf.uri == pers.viaf_id

    def test_set_birth_death_years(self):
        pers = Person(authorized_name='Humperdinck')
        # no viaf id
        pers.set_birth_death_years()
        assert pers.birth is None
        assert pers.death is None

        pers.viaf_id = 'http://viaf.org/viaf/35247539'
        with patch.object(Person, 'viaf') as mockviaf_entity:
            mockviaf_entity.birthyear = 1902
            mockviaf_entity.deathyear = 1953
            pers.set_birth_death_years()
            assert pers.birth == mockviaf_entity.birthyear
            assert pers.death == mockviaf_entity.deathyear

    def test_save(self):
        pers = Person(authorized_name='Humperdinck')
        with patch.object(pers, 'set_birth_death_years') as mock_setbirthdeath:
            # no viaf - should not call set birth/death
            pers.save()
            mock_setbirthdeath.assert_not_called()

            # viaf and dates set - should not call set birth/death
            pers.viaf_id = 'http://viaf.org/viaf/35247539'
            pers.birth = 1801
            pers.death = 1850
            pers.save()
            mock_setbirthdeath.assert_not_called()

            # viaf and one date set - should not call set birth/death
            pers.birth = None
            pers.save()
            mock_setbirthdeath.assert_not_called()

            # viaf and no dates set - *should* call set birth/death
            pers.death = None
            pers.save()
            mock_setbirthdeath.assert_called_with()

    def test_firstname_last(self):
        # convert authorized name to firstname last
        pers = Person(authorized_name='Granger, Gilles-Gaston')
        assert pers.firstname_last == 'Gilles-Gaston Granger'
        # single name, should that occur
        pers.authorized_name = 'Humperdinck'
        assert pers.firstname_last == pers.authorized_name

    def test_lastname(self):
        # extract lastname from authorized name
        pers = Person(authorized_name='Granger, Gilles-Gaston')
        assert pers.lastname == 'Granger'
        # single name, should that occur
        pers.authorized_name = 'Humperdinck'
        assert pers.lastname == pers.authorized_name


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


class TestPersonAutocomplete(TestCase):

    password = uuid.uuid4()

    def setUp(self):
        User = get_user_model()
        User.objects.create_superuser(
            username='test',
            password=self.password,
            email='foo@bar.com'
        )
        Person.objects.create(
            authorized_name='Mr. Author'
        )

    def test_view_behavior(self):
        # No login for anonymous user
        response = self.client.get(reverse('books:publisher-autocomplete'))
        assert response.status_code == 302

        # Get a response as a staff user
        self.client.login(username='test', password=self.password)
        response = self.client.get(
            reverse('people:person-autocomplete'),
            params={'q': 'Mr.'}
        )
        assert response.status_code == 200
        data = json.loads(response.content.decode('utf-8'))
        assert 'results' in data
        assert data['results'][0]['text'] == 'Mr. Author'
