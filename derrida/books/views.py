from dal import autocomplete
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from haystack.query import SearchQuerySet

from .forms import ReferenceSearchForm, InstanceSearchForm, SearchForm
from .models import Publisher, Language, Instance, Reference, DerridaWorkSection
from derrida.interventions.models import Intervention


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
    slug_field = 'slug'

    def get_queryset(self):
        instances = super(InstanceDetailView, self).get_queryset()
        return instances.filter(digital_edition__isnull=False)


class InstanceReferenceDetailView(InstanceDetailView):

    template_name = 'books/detail/citations.html'

    def get_context_data(self, *args, **kwargs):
        context = super(InstanceReferenceDetailView, self)\
            .get_context_data(*args, **kwargs)
        refs = SearchQuerySet().models(Reference) \
            .filter(instance_slug=self.object.slug)
        context['references'] = refs

        # sorting todo
        return context


class InstanceListView(ListView):
    # NOTE: haystack includes generic views, but they are not well documented
    # and don't seem to work quite right, so sticking with stock django
    # class-based views and forms.

    model = Instance
    form_class = InstanceSearchForm
    paginate_by = 16
    template_name = 'books/instance_list.html'

    def get_queryset(self):
        sqs = SearchQuerySet().models(self.model)
        # restrict to extant books
        sqs = sqs.filter(is_extant=True, item_type='Book')

        # if search parameters are specified, use them to initialize the form;
        # otherwise, use form defaults
        self.form = self.form_class(self.request.GET or
                                    self.form_class.defaults)

        for facet_field in self.form.facet_fields:
            # sort by alpha instead of solr default of count
            sqs = sqs.facet(facet_field, sort='index')
        # form shouldn't normally be invalid since no fields are
        # required, but cleaned data isn't available until we validate
        if self.form.is_valid():
            search_opts = self.form.cleaned_data
        else:
            # fallback to defaults (i.e. sort only)
            search_opts = self.form.defaults

        # filter solr query based on search options
        if search_opts.get('query', None):
            sqs = sqs.filter(text=search_opts['query'])
        # if search_opts.get('is_extant', None):
            # sqs = sqs.filter(is_extant=search_opts['is_extant'])
        if search_opts.get('is_annotated', None):
            sqs = sqs.filter(is_annotated=search_opts['is_annotated'])
        for facet in self.form.facet_fields:
            if facet in search_opts and search_opts[facet]:
                sqs = sqs.filter(**{'%s__in' % facet: search_opts[facet]})
        # sort should always be set
        if search_opts['order_by']:
            sqs = sqs.order_by(search_opts['order_by'])

        return sqs

    def get_context_data(self, **kwargs):
        context = super(InstanceListView, self).get_context_data(**kwargs)
        sqs = self.get_queryset()
        facets = sqs.facet_counts()
        # update multi-choice fields based on facets in the data
        self.form.set_choices_from_facets(facets.get('fields'))
        context.update({
            'facets': facets,
            'total': sqs.count(),
            'form': self.form
        })
        return context


class ReferenceListView(ListView):
    # full reference list; eventually will have filter/sort options

    model = Reference
    form_class = ReferenceSearchForm
    paginate_by = 16
    template_name = 'books/reference_list.html'

    def get_queryset(self):
        sqs = SearchQuerySet().models(self.model)

        # if search parameters are specified, use them to initialize the form;
        # otherwise, use form defaults
        self.form = self.form_class(self.request.GET or None)
        for facet_field in self.form.facet_fields:
            sqs = sqs.facet(facet_field)

        if self.form.is_valid():
            search_opts = self.form.cleaned_data
        else:
            # todo: display/handle any form validation errors
            # (possible?)
            # for now, return unfiltered queryset with facets
            return sqs

        # filter solr query based on search options
        if search_opts['query']:
            sqs = sqs.filter(text=search_opts['query'])

        for facet in self.form.facet_fields:
            if facet in search_opts and search_opts[facet]:
                sqs = sqs.filter(**{'%s__in' % facet: search_opts[facet]})

        return sqs

    def get_context_data(self, **kwargs):
        context = super(ReferenceListView, self).get_context_data(**kwargs)
        sqs = self.get_queryset()
        facets = sqs.facet_counts()
        # update multi-choice fields based on facets in the data
        self.form.set_choices_from_facets(facets.get('fields'))
        context.update({
            'facets': facets,
            'total': sqs.count(),
            'form': self.form,
        })
        return context


class ReferenceHistogramView(ListView):
    template_name = 'books/reference_histogram.html'
    model = Reference

    def get_queryset(self):
        refs = super(ReferenceHistogramView, self).get_queryset()
        # sort based on specified mode
        # TODO: filter on specific derrida work, for when we have more than one?
        if self.kwargs.get('mode', None) == 'section':
            refs = refs.order_by_source_page()
        else:
            refs = refs.order_by_author()
        return refs.summary_values()

    def get_context_data(self):
        context = super(ReferenceHistogramView, self).get_context_data()
        if self.kwargs.get('mode', None) == 'section':
            # get sections for the specified derrida work
            sections = DerridaWorkSection.objects \
                .filter(derridawork__slug=self.kwargs['derridawork_slug'])
            context.update({
                'mode': self.kwargs['mode'],
                'sections': sections
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


class SearchView(TemplateView):
    form_class = SearchForm
    template_name = 'books/search.html'
    max_per_type = 3

    def get(self, *args, **kwargs):
        self.form = self.form_class(self.request.GET)
        # if search on a single type is requested, forward to the
        # appropriate view
        if self.form.is_valid():
            search_opts = self.form.cleaned_data
            if search_opts['content_type'] != 'all':
                if search_opts['content_type'] == 'book':
                    url = reverse('books:list')
                elif search_opts['content_type'] == 'reference':
                    url = reverse('books:reference-list')
                elif search_opts['content_type'] == 'intervention':
                    url = reverse('interventions:list')

                url = '%s?query=%s' % (url, search_opts['query'])
                response = HttpResponseRedirect(url)
                response.status_code = 303  # see other
                return response

        return super(SearchView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        search_opts = self.form.cleaned_data
        sqs = SearchQuerySet().filter()

        if search_opts['query']:
            sqs = sqs.filter(text=search_opts['query'])

        # NOTE: Solr supports grouping results in a single search, but
        # haystack does not.  For now, query each content type separately.

        instance_query = sqs.models(Instance).all()
        reference_query = sqs.models(Reference).all()
        intervention_query = sqs.models(Intervention).all()

        return {
            'query': search_opts['query'],
            'instance_list': instance_query[:self.max_per_type],
            'instance_count': instance_query.count(),
            'reference_list': reference_query[:self.max_per_type],
            'reference_count': reference_query.count(),
            'intervention_list': intervention_query[:self.max_per_type],
            'intervention_count': intervention_query.count()
            # outwork TODO
        }
