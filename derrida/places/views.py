from django.http import JsonResponse
from dal import autocomplete
from .geonames import GeoNamesAPI
from .models import Place


class PlaceAutocomplete(autocomplete.Select2QuerySetView):
    '''Basic place ajax autocomplete lookup, based on
    django-autocomplete-light.
    Currently restricted to staff only.'''
    # staff restruction in url config

    def get_queryset(self):
        return Place.objects.filter(name__istartswith=self.q)


class GeonamesLookup(autocomplete.Select2ListView):
    '''GeoNames ajax lookup for use as autocomplete.
    Currently restricted to staff only.'''

    def get(self, request, *args, **kwargs):
        """"Return option list json response."""
        geo_api = GeoNamesAPI()
        results = geo_api.search(self.q, max_rows=50)
        return JsonResponse({
            'results': [dict(
                id=geo_api.uri_from_id(item['geonameId']),
                text=self.get_label(item),
                name=item['name'],
                # lat & long included in data to make them available for
                # javascript to populateform fields
                lat=item['lat'],
                lng=item['lng']
            ) for item in results],
        })

    def get_label(self, item):
        # display country for context, if available
        if 'countryName' in item:
            return '''%(name)s, %(countryName)s''' % item
        return item['name']
