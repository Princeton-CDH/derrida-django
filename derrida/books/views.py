from dal import autocomplete
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from haystack.query import SearchQuerySet

from .forms import CitationSearchForm, InstanceSearchForm, SearchForm
from .models import Publisher, Language, Instance, Reference, DerridaWorkSection


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
        if search_opts['is_extant']:
            sqs = sqs.filter(is_extant=True)
        if search_opts['is_annotated']:
            sqs = sqs.filter(is_annotated=True)

        for facet in self.form.facet_fields:
            if facet in search_opts and search_opts[facet]:
                sqs = sqs.filter(**{'%s__in' % facet: search_opts[facet]})

        # disabling sort for now (issues/questions TBD)
        # if search_opts['order_by']:
            # sqs = sqs.order_by(search_opts['order_by'])

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
            'form': self.form,
        })
        return context


class ReferenceListView(ListView):
    # full citation/reference list; eventually will have filter/sort options
    # (sticking with 'reference' for now until project team confirms
    # which term is more general / preferred for public site)

    # NOTE: Still leaving this as Reference, but perhaps it should change since
    # citation is firmly in place on the public site?

    model = Reference
    form_class = CitationSearchForm
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

        return {
            'query': search_opts['query'],
            'instance_list': instance_query[:self.max_per_type],
            'instance_count': instance_query.count(),
            'reference_list': reference_query[:self.max_per_type],
            'reference_count': reference_query.count()
            # annotations todo
            # outwork TODO
        }
