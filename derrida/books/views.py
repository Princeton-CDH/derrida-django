import json

from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db.models import Max, Min
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from djiffy.models import Canvas
from haystack.query import SearchQuerySet
from haystack.inputs import Clean, Raw
import requests

from derrida.books.forms import ReferenceSearchForm, InstanceSearchForm, \
    SearchForm, SuppressImageForm
from derrida.books.models import Publisher, Language, Instance, Reference, DerridaWorkSection
from derrida.common.utils import absolutize_url
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

        sort = self.request.GET.get('order_by', None)
        if sort == 'book_page':
            refs = refs.order_by('book_page_exact')
            context['order_by'] = 'book_page'
        else:
            refs = refs.order_by('derridawork_page')

        context['references'] = refs
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
        print('query = %s' % sqs.query)
        # restrict to extant books that are cited
        sqs = sqs.filter(is_extant=True, item_type_exact='Book',
                         cited_in='*')
        # Note: using item_type_exact to avoid matching book section

        # if search parameters are specified, use them to initialize the form;
        # otherwise, use form defaults
        self.form = self.form_class(self.request.GET or
                                    self.form_class.defaults)

        # request facet counts from solr
        for facet_field in self.form.facet_fields:
            # sort by alpha instead of solr default of count
            sqs = sqs.facet(facet_field, sort='index')

        # request range facets
        # TODO: only get max/min from db when not specified in query opts
        # (can/should we cache these?)
        # get max/min from database
        ranges = Instance.objects.filter(is_extant=True, reference__isnull=False) \
            .aggregate(work_year_max=Max('work__year'), work_year_min=Min('work__year'),
                copyright_year_max=Max('copyright_year'), copyright_year_min=Min('copyright_year'),
                print_year_max=Max('print_date'), print_year_min=Min('print_date'))
        for range_facet in self.form.range_facets:
            range_opts = {
                'start': ranges['%s_min' % range_facet],
                'end': ranges['%s_max' % range_facet],
                'gap': 100  # ???
            }
            if range_facet == 'print_year':
                # special case: print year is a datetime but we only want year
                range_opts['start'] = range_opts['start'].year if range_opts['start'] else None
                range_opts['end'] = range_opts['end'].year if range_opts['end'] else None
            # TODO: caalculate gap based on the desired number of slices
            sqs = sqs.facet(range_facet, range=True, **range_opts)

        # form shouldn't normally be invalid since no fields are
        # required, but cleaned data isn't available until we validate
        if self.form.is_valid():
            search_opts = self.form.cleaned_data
        else:
            # fallback to defaults (i.e. sort only)
            search_opts = self.form.defaults

        # filter solr query based on search options
        if search_opts.get('query', None):
            sqs = sqs.filter(content=Clean(search_opts['query']))
        # no is extant filter for library; already restricted to extant items
        if search_opts.get('is_annotated', None):
            sqs = sqs.filter(is_annotated=search_opts['is_annotated'])

        for facet in self.form.facet_inputs:
            # check if a value is set for this facet
            if facet in search_opts and search_opts[facet]:
                solr_facet = self.form.solr_field(facet)
                # filter the query: facet matches any of the terms
                sqs = sqs.filter(**{'%s__in' % solr_facet: search_opts[facet]})

        for range_facet in self.form.range_facets:
            if range_facet in search_opts and search_opts[range_facet]:
                start, end = search_opts[range_facet].split('-')
                # could have both start and end or just one
                # NOTE: haystack includes a range field lookup, but
                # it converts numbers to strings, so this is easier
                range_filter = '[%s TO %s]' % (start or '*', end or '*')
                sqs = sqs.filter(**{range_facet: Raw(range_filter)})

        # sort should always be set
        if search_opts['order_by']:
            # convert sort option to corresponding solr field
            solr_sort = self.form.solr_field(search_opts['order_by'])
            sqs = sqs.order_by(solr_sort)

        # store for retrieving facets in get context data
        self.queryset = sqs
        return sqs

    def get_context_data(self, **kwargs):
        context = super(InstanceListView, self).get_context_data(**kwargs)
        facets = self.queryset.facet_counts()
        # update multi-choice fields based on facets in the data
        self.form.set_choices_from_facets(facets.get('fields'))
        context.update({
            'facets': facets,   # now includes ranges as facets.ranges
            'total': self.queryset.count(),
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
        self.form = self.form_class(self.request.GET or \
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
            sqs = sqs.filter(text=Clean(search_opts['query']))

        if search_opts.get('is_extant', None):
            sqs = sqs.filter(instance_is_extant=search_opts['is_extant'])
        if search_opts.get('is_annotated', None):
            sqs = sqs.filter(instance_is_annotated=search_opts['is_annotated'])
        if search_opts.get('corresponding_intervention', None):
            sqs = sqs.filter(corresponding_intervention=search_opts['corresponding_intervention'])

        # look over form fields that map to facets
        for facet in self.form.facet_inputs:
            # check if a value is set for this facet
            if facet in search_opts and search_opts[facet]:
                solr_facet = self.form.solr_field(facet)
                # filter the query: facet matches any of the terms
                sqs = sqs.filter(**{'%s__in' % solr_facet: search_opts[facet]})

        # sort should always be set
        if search_opts['order_by']:
            # convert sort option to corresponding solr field
            solr_sort = self.form.solr_field(search_opts['order_by'])
            sqs = sqs.order_by(solr_sort)

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
        # NOTE: eventually this willl need to filter/segment
        # on derrida work, when we have more than one.
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
        # NOTE: this is returning two results for some cases
        # (seems to be an error in the data; just return the first match)
        return queryset.filter(
            derridawork_page=self.kwargs['page'],
            derridawork_pageloc=self.kwargs['pageloc'],
            derridawork__slug=self.kwargs['derridawork_slug']
            ).first()


class SearchView(TemplateView):
    form_class = SearchForm
    template_name = 'books/multi_search.html'
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


class CanvasDetail(DetailView):
    model = Canvas
    template_name = 'books/public_canvas_detail.html'

    def get_object(self, queryset=None):
        self.instance = get_object_or_404(Instance, slug=self.kwargs['slug'])
        canvas = self.instance.images() \
            .filter(short_id=self.kwargs['short_id']).first()

        # only show canvas detail page for insertions, overview images,
        # and pages with documented interventions
        if canvas and Instance.allow_canvas_detail(canvas):
            return canvas
        else:
            raise Http404

    def get_context_data(self, *args, **kwargs):
        context = super(CanvasDetail, self).get_context_data(*args, **kwargs)
        context.update({
            'instance': self.instance,
            'canvas_suppressed': self.instance.suppress_all_images or \
                    self.object in self.instance.suppressed_images.all()
        })
        if self.request.user.has_perm('books.change_instance'):
            context.update({
                'suppress_form': SuppressImageForm(initial={'canvas_id': self.object.short_id}),
            })
        return context


class CanvasSuppress(FormView):
    '''Form view to process an admin request to suppress a single
    canvas image or all annotated pages from a volume.  Requires
    user to have change_instance permission.'''
    form_class = SuppressImageForm

    @method_decorator(permission_required('books.change_instance'))
    def dispatch(self, *args, **kwargs):
        return super(CanvasSuppress, self).dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        # no get display; redirect to book detail
        response = HttpResponseRedirect(reverse('books:detail',
            kwargs={'slug': self.kwargs['slug']}))
        response.status_code = 303  # see other
        return response

    def form_valid(self, form):
        # process valid POSTed form data
        formdata = form.cleaned_data
        instance = get_object_or_404(Instance, slug=self.kwargs['slug'])

        # suppress current page or all pages
        if formdata['suppress'] == 'current':
            canvas = Canvas.objects.get(short_id=formdata['canvas_id'])
            instance.suppressed_images.add(canvas)
            msg = 'Canvas successfully suppressed.'
        else:
            instance.suppress_all_images = True
            msg = 'Successfully suppressed all annotated pages for this instance.'
        instance.save()
        messages.success(self.request, msg)

        # Redirect to canvas detail view
        response = HttpResponseRedirect(reverse('books:canvas-detail',
            kwargs={'slug': self.kwargs['slug'],
                    'short_id': formdata['canvas_id']}))
        response.status_code = 303  # see other
        return response


class ProxyView(View):
    # ProxyView, modeled on Django's RedirectView
    # adapted from the Readux codebase (readux.books.views)

    def get(self, request, *args, **kwargs):
        url = self.get_proxy_url(*args, **kwargs)
        # use headers to allow browsers to cache downloaded copies
        headers = {}
        for header in ['HTTP_IF_MODIFIED_SINCE', 'HTTP_IF_UNMODIFIED_SINCE',
                       'HTTP_IF_MATCH', 'HTTP_IF_NONE_MATCH']:
            if header in request.META:
                headers[header.replace('HTTP_', '')] = request.META.get(header)
        remote_response = requests.get(url, headers=headers)
        local_response = HttpResponse()
        local_response.status_code = remote_response.status_code

        # include response headers, except for server-specific items
        for header, value in remote_response.headers.items():
            if header not in ['Connection', 'Server', 'Keep-Alive', 'Link']:
                             # 'Access-Control-Allow-Origin', 'Link']:
                # NOTE: link header is valuable, but would
                # need to be made relative to current url
                local_response[header] = value

        # special case, for deep zoom (hack)
        if kwargs['mode'] == 'info':
            data = remote_response.json()
            # need to adjust the id to be relative to current url
            # this is a hack, patching in a proxy iiif interface at this url
            data['@id'] = absolutize_url(request.path.replace('/info/', '/iiif'),
                request)

            local_response.content = json.dumps(data)
            # upate content-length for change in data
            local_response['content-length'] = len(local_response.content)
            # needed to allow external site (i.e. jekyll export)
            # to use deepzoom
            local_response['Access-Control-Allow-Origin'] = '*'
        else:
            # include response content if any
            local_response.content = remote_response.content

        return local_response

    def head(self, request, *args, **kwargs):
        url = self.get_proxy_url(*args, **kwargs)
        remote_response = requests.head(url)
        response = HttpResponse()
        for header, value in remote_response.headers.iteritems():
            if header not in ['Connection', 'Server', 'Keep-Alive',
                             'Access-Control-Allow-Origin', 'Link']:
                response[header] = value
        return response


class CanvasImageByPageNumber(View):
    '''Get a canvas image from an :class:`~derrida.books.models.Instance`
    by page number. Searches by page label, if no match is found returns
    the thumbnail for the Item if there is one.  404 if not found or
    the Instance has no digital edition associated.'''
    def get(self, request, *args, **kwargs):
        self.instance = get_object_or_404(Instance, slug=self.kwargs['slug'])
        # look up canvas for requested page number in this item
        page = 'p. %s' % self.kwargs['page_num']
        if self.instance.digital_edition:
            canvas = self.instance.images().filter(label__exact=page).first()
            # if page is not found, fallback to book cover
            if not canvas:
                canvas = self.instance.digital_edition.thumbnail

            # if we have a canvas, redirect to thumbnail image view
            if canvas and canvas.short_id:
                canvas_url = reverse('books:canvas-image',
                    kwargs={'slug': self.kwargs['slug'],
                            'short_id': canvas.short_id, 'mode': 'thumbnail'})

                response = HttpResponseRedirect(canvas_url)
                response.status_code = 303  # see other
                return response

        # 404 if no canvas was found
        raise Http404


class CanvasImage(ProxyView):
    '''Local view for canvas images.  This proxies the
    configured IIIF image viewer in order to avoid exposing IIIF image
    urls for copyright content and to allow controlled access
    to restrict public viewable material to annotated pages,
    overview images, and insertions.'''

    def get_proxy_url(self, *args, **kwargs):
        instance = get_object_or_404(Instance, slug=self.kwargs['slug'])
        canvas_id = self.kwargs.get('short_id', None)
        if canvas_id:
            canvas = instance.images() \
                .filter(short_id=self.kwargs['short_id']).first()
        else:
            canvas = instance.digital_edition.thumbnail

        if not canvas:
            raise Http404

        if kwargs['mode'] == 'thumbnail':
            return canvas.image.thumbnail()

        if kwargs['mode'] == 'large':
            # only allow large images for insertions, overview images,
            # and pages with documented interventions
            # - also checks if an image has been suppressed
            if not instance.allow_canvas_large_image(canvas):
                raise Http404

            return canvas.image.size(height=850, width=850,
                exact=True)    # exact = preserve aspect

        if kwargs['mode'] == 'info':
            return canvas.image.info()
        elif kwargs['mode'] == 'iiif':
            # also restrict iiif tiles based on large image permission
            if not instance.allow_canvas_large_image(canvas):
                raise Http404
            return canvas.image.info().replace('info.json', kwargs['url'].strip('/'))



