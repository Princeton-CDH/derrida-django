from dal import autocomplete

from .models import Publisher, Language, Instance, Reference, DerridaWorkSection

from django.views.generic import DetailView, ListView


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


class InstanceDetailView(DetailView):
    ''':class:`~django.views.generic.DetailView` for
    :class:`~derrida.books.models.Instance`. Returns only Instances that have
    digtial editions set.'''

    model = Instance

    def get_queryset(self):
        instances = super(InstanceDetailView, self).get_queryset()
        return instances.filter(digital_edition__isnull=False)


class InstanceListView(ListView):
    '''View that provides a paginated, potentially filterable list of
    :class:`~derrida.books.models.Instance`. Users pagination functionality
    provided by :class:`~django.views.generic.ListView` to provide pagination
    by query string `?page=`'''

    model = Instance
    paginate_by = 16

    def get_queryset(self):
        instances = super(InstanceListView, self).get_queryset()
        order = self.request.GET.get('orderBy', 'work__authors__authorized_name')
        return instances.order_by(order)

    def get_context_data(self, **kwargs):
        context = super(InstanceListView, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        context['orderBy'] = self.request.GET.get('orderBy', 'work__authors__authorized_name')

        return context

class ReferenceListView(ListView):
    # full citation/reference list; eventually will have filter/sort options
    # (sticking with 'reference' for now until project team confirms
    # which term is more general / preferred for public site)
    model = Reference
    paginate_by = 16

    # default ordering by derrida work, page, page location
    # matches default ordering for this view


class ReferenceHistogramView(ListView):
    template_name = 'books/reference_histogram.html'
    model = Reference

    def get_queryset(self):
        refs = super(ReferenceHistogramView, self).get_queryset()
        # for now, returning references by author; eventually
        # we'll also want references by section of derrida work
        # return a values list that can be regrouped in the template
        if self.kwargs.get('mode', None) == 'section':
            sort = 'derridawork_page'
        else:
            sort = 'instance__work__authors__authorized_name'

        return refs.order_by(sort) \
                   .values('id', 'instance__work__authors__authorized_name',
                           'instance',
                           'derridawork__slug', 'derridawork_page',
                           'derridawork_pageloc')

    def get_context_data(self):
        context = super(ReferenceHistogramView, self).get_context_data()
        if self.kwargs.get('mode', None) == 'section':
            context.update({
                'mode': self.kwargs['mode'],
                'sections': DerridaWorkSection.objects.filter(derridawork__slug=self.kwargs['derridawork_slug'])
            })

        return context


class ReferenceDetailView(DetailView):
    # reference detail view for loading via ajax

    model = Reference
    template_name = 'components/citation-list-item.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        # FIXME: this is returning two results for some cases
        # (must be an error in the data)
        # return queryset.get(derridawork_page=self.kwargs['page'],
        return queryset.filter(
            derridawork_page=self.kwargs['page'],
            derridawork_pageloc=self.kwargs['pageloc'],
            derridawork__slug=self.kwargs['derridawork_slug']
            ).first()


