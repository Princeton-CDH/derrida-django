from dal import autocomplete

from .models import Publisher, Language, Instance

from django.views.generic import ListView

class PublisherAutocomplete(autocomplete.Select2QuerySetView):
    '''Basic publisher autocomplete lookup, for use with
    django-autocomplete-light.  Restricted to staff only.'''
    # NOTE staff restriction applied in url config

    def get_queryset(self):
        return Publisher.objects.filter(name__icontains=self.q)


class LanguageAutocomplete(autocomplete.Select2QuerySetView):
    '''Autocomplete lookup for :class:`derrida.books.models.Language`, for use with
    django-autocomplete-light.  Restricted to staff only.'''
    # NOTE staff restriction applied in url config

    def get_queryset(self):
        return Language.objects.filter(name__icontains=self.q)


class InstanceListView(ListView):
    '''View that provides a paginated, potentially filterable list of
    :class:`~derrida.books.models.Instance`'''

    model = Instance
    paginate_by = 16

    def get_queryset(self):
        return super(InstanceListView, self).get_queryset().order_by('work__authors__authorized_name')
