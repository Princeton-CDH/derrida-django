from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.test import TestCase, override_settings
from django.urls import reverse
import json

from .admin import GeonamesLookupWidget
from .models import Place
from .geonames import GeoNamesAPI
from .views import GeonamesLookup


class TestPlace(TestCase):

    def test_str(self):
        nyc = Place(name='New York City')
        assert str(nyc) == 'New York City'


@override_settings(GEONAMES_USERNAME='test_geonames_user')
class TestGeonamesApi(TestCase):

    fixtures = ['test_place_data.json']

    def test_init(self):
        geo_api = GeoNamesAPI()
        # username should be set from django config
        assert geo_api.username == 'test_geonames_user'

    @patch('derrida.places.geonames.requests')
    def test_search(self, mockrequests):
        geo_api = GeoNamesAPI()

        mock_result = {'geonames': []}

        mockrequests.get.return_value.json.return_value = mock_result
        result = geo_api.search('amsterdam')
        assert result == []
        mockrequests.get.assert_called_with('http://api.geonames.org/searchJSON',
            params={'username': 'test_geonames_user', 'q': 'amsterdam'})

        # with max specified
        result = geo_api.search('london', max_rows=20)
        mockrequests.get.assert_called_with('http://api.geonames.org/searchJSON',
            params={'username': 'test_geonames_user', 'q': 'london',
                    'maxRows': 20})

    def test_uri_from_id(self):
        assert GeoNamesAPI.uri_from_id(12345) == \
            'http://sws.geonames.org/12345/'


class TestPlaceViews(TestCase):

    fixtures = ['test_place_data.json']

    def setUp(self):
        # create an admin user to test autocomplete views
        self.password = 'pass!@#$'
        self.admin = get_user_model().objects.create_superuser('testadmin',
            'test@example.com', self.password)

    def test_place_autocomplete(self):
        pl_autocomplete_url = reverse('places:autocomplete')
        result = self.client.get(pl_autocomplete_url,
            params={'q': 'fran'})
        # not allowed to anonymous user
        assert result.status_code == 302

        # login as an admin user
        self.client.login(username=self.admin.username, password=self.password)

        result = self.client.get(pl_autocomplete_url, {'q': 'fran'})
        assert result.status_code == 200
        # decode response to inspect
        data = json.loads(result.content.decode('utf-8'))
        assert data['results'][0]['text'] == 'Frankfurt'

    @patch('derrida.places.views.GeoNamesAPI')
    def test_geonames_autocomplete(self, mockgeonamesapi):
        geo_autocomplete_url = reverse('places:geonames-autocomplete')
        result = self.client.get(geo_autocomplete_url,
            params={'q': 'amsterdam'})
        # not allowed to anonymous user
        assert result.status_code == 302

        # login as an admin user
        self.client.login(username=self.admin.username, password=self.password)

        # abbreviated sample return with fields currently in use
        mock_response = [
            {'name': 'New York City', 'geonameId': 5128581,
             'countryName': 'USA', 'lat': 40.71427, 'lng': -74.00597}
        ]

        mockgeonamesapi.return_value.search.return_value = mock_response
        # patch in real uri from id logic
        mockgeonamesapi.return_value.uri_from_id = GeoNamesAPI.uri_from_id

        result = self.client.get(geo_autocomplete_url,
            params={'q': 'new york'})
        assert isinstance(result, JsonResponse)
        assert result.status_code == 200
        # decode response to inspect
        data = json.loads(result.content.decode('utf-8'))
        # inspect constructed result
        item = data['results'][0]
        assert item['text'] == 'New York City, USA'
        assert item['name'] == 'New York City'
        assert item['lat'] == mock_response[0]['lat']
        assert item['lng'] == mock_response[0]['lng']
        assert item['id'] == \
            GeoNamesAPI.uri_from_id(mock_response[0]['geonameId'])

    def test_get_label(self):
        geo_lookup = GeonamesLookup()
        item = {'name': 'New York City', 'countryName': 'USA'}
        # country code used if available
        assert geo_lookup.get_label(item) == 'New York City, USA'
        del item['countryName']
        # and just name, if no country is available
        assert geo_lookup.get_label(item) == 'New York City'


class TestGeonamesLookupWidget(TestCase):

    def test_render(self):
        widget = GeonamesLookupWidget()
        # no value set - should not error
        rendered = widget.render('place', None, {'id': 'place'})
        assert '<p><a id="geonames_uri" target="_blank" href=""></a></p>' \
            in rendered
        # uri value set - should be included in generated link
        uri = 'http://sws.geonames.org/2759794/'
        rendered = widget.render('place', uri, {'id': 'place'})
        assert '<a id="geonames_uri" target="_blank" href="%(uri)s">%(uri)s</a>' \
            % {'uri': uri} in rendered
        # value should be set as an option to preserve existing
        # value when the form is submitted
        assert '<option value="%(uri)s" selected>%(uri)s</option' % \
            {'uri': uri} in rendered

