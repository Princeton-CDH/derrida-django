from dal import autocomplete
from .models import Person


class PersonAutocomplete(autocomplete.Select2QuerySetView):
    '''Basic person autocomplete lookup, for use with
    django-autocomplete-light.  Restricted to staff only.'''
    # NOTE staff restrection applied in url config

    def get_queryset(self):
        return Person.objects.filter(authorized_name__icontains=self.q)
