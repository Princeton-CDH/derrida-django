from django.http import JsonResponse
from dal import autocomplete
from .models import Person
from .viaf import ViafAPI


class ViafAutoSuggest(autocomplete.Select2ListView):
    """ View to provide VIAF suggestions for autocomplete info"""

    def get(self, request, *args, **kwargs):
        """Return JSON with suggested VIAF ids and display names."""
        viaf = ViafAPI()
        result = viaf.suggest(self.q)
        # Strip names that are not personal
        for item in result:
            if item['nametype'] is not 'personal':
                del item
        return JsonResponse({
            'results': [dict(
                id=viaf.uri_from_id(item['viafid']),
                text=(item['displayForm']),
            ) for item in result],
        })


class PersonAutocomplete(autocomplete.Select2QuerySetView):
    '''Basic person autocomplete lookup, for use with
    django-autocomplete-light.  Restricted to staff only.'''
    # NOTE staff restrection applied in url config

    def get_queryset(self):
        return Person.objects.filter(authorized_name__icontains=self.q)
