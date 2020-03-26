from django.conf import settings
import requests


class GeoNamesAPI(object):
    '''Minimal wrapper around GeoNames API.  Currently supports simple
    searching by name and generating a uri from an id.  Expects
    **GEONAMES_USERNAME** to be configured in django settings.'''

    api_base = 'http://api.geonames.org'

    def __init__(self):
        self.username = getattr(settings, "GEONAMES_USERNAME", None)

    def search(self, query, max_rows=None):
        '''Search for places and return the list of results'''
        api_url = '%s/%s' % (self.api_base, 'searchJSON')
        params = {'username': self.username, 'q': query}
        if max_rows is not None:
            params['maxRows'] = max_rows
        response = requests.get(api_url, params=params)
        # return the list of results (present even when empty)
        return response.json()['geonames']

    @classmethod
    def uri_from_id(cls, geonames_id):
        '''Convert a GeoNames id into a GeoNames URI'''
        return 'http://sws.geonames.org/%d/' % geonames_id
