import datetime
import json

from dal import autocomplete
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Max, Min
from django.views.generic import ListView
from djiffy import views as djiffy_views
from haystack.inputs import Raw
from haystack.query import SearchQuerySet

from derrida.books.models import Language
from derrida.common.solr_backend import facet_sort_ignoreaccents
from derrida.interventions.models import Intervention, Tag, get_default_intervener
from derrida.interventions.forms import InterventionSearchForm
from derrida.people.models import Person


class TagAutocomplete(autocomplete.Select2QuerySetView):
    '''Autocomplete view for :class:`~derrida.intervention.models.Tag`
    to use in association with :class:`~derrida.intervention.models.Intervention`'''
    def get_queryset(self):
        tags = Tag.objects.filter(name__icontains=self.q)

        # if mode is specified, filter tags accordingly
        if 'mode' in self.kwargs:
            if self.kwargs['mode'] == 'annotation':
                tags = tags.for_annotations()
            elif self.kwargs['mode'] == 'insertion':
                tags = tags.for_insertions()

        return tags


class LoginPermissionRequired(PermissionRequiredMixin):
    '''Customization of :class:`django.contrib.auth.mixins.PermissionRequiredMixin`
    that redirects to the configured login url if the user is not authenticated,
    and raises a 403 Forbidden if they already are authenticated.'''

    # NOTE: django provides a raise_exception to raise a 403 rather
    # than prompting login, but there is no way to set that for the
    # permission without also setting it for the login required check.
    # raise_exception = True  # raise 403 rather than prompting login

    # override handle no permissions to raise 403 *only* if the
    # user is not authenticated; otherwise redirect to login page normally
    # adapted from https://github.com/brack3t/django-braces/issues/88
    def handle_no_permission(self):
        if self.request and self.request.user.is_authenticated():
            raise PermissionDenied
        return super(LoginPermissionRequired, self).handle_no_permission()


class ManifestList(LoginPermissionRequired, djiffy_views.ManifestList):
    permission_required = 'djiffy.view_manifest'


class ManifestDetail(LoginPermissionRequired, djiffy_views.ManifestDetail):
    permission_required = 'djiffy.view_manifest'


class CanvasDetail(LoginPermissionRequired, djiffy_views.CanvasDetail):
    permission_required = 'djiffy.view_canvas'

    def get_context_data(self, **kwargs):
        context = super(CanvasDetail, self).get_context_data(**kwargs)
        # pass in list of languages for use in annotator edit form
        languages = list(Language.objects.all().values_list('name', flat=True))
        # insert a blank option, since language is optional
        languages.insert(0, '')
        context['languages_js'] = json.dumps(languages)
        # pass in default authorized name for Derrida, if he exists, else a
        # literal '' for annotator_init.html
        default_intervener_pk = get_default_intervener()
        context['default_intervener'] = json.dumps('')
        if default_intervener_pk:
            context['default_intervener'] = json.dumps(
                (Person.objects.get(pk=default_intervener_pk)).authorized_name)
        return context


class CanvasAutocomplete(LoginPermissionRequired, djiffy_views.CanvasAutocomplete):
    """Override the default
    :class:`~djiffy.views.CanvasAutocomplete.get_queryset()` in order to
    allow forms that specify an :class:`~derrida.books.models.Instance`
    object to filter based on annotations associated only
    with that instance.

    This lets instances of :class:`~django.forms.ModelForm` that have a
    :class:`~djiffy.models.Canvas` autocomplete pass a set instance
    value to restrict autocomplete results only to the Instance currently
    being edited.

    :class:`dal.autocomplete.Select2QuerySetView` allows a ``forward``
    parameter that passes JSON object as a string after as a query string
    named ``forward``.
    :method:`dal.autocomplete.Select2QuerySetView.forwarded.get()` can
    access those variables easily.

    The autocomplete looks for an instance primary key passed with the key
    ``instance`` in the JSON object.
    """
    permission_required = 'djiffy.view_canvas'

    def get_queryset(self):
        query = super(CanvasAutocomplete, self).get_queryset()
        # Add an extra filter based on the forwarded value of 'instance',
        # if provided
        instance = self.forwarded.get('instance', None)
        if instance:
            query = query.filter(manifest__instance__pk=instance)
        # filter on manifest id if present
        manifest_id = self.forwarded.get('manifest', None)
        if manifest_id:
            query = query.filter(manifest__pk=manifest_id)
        return query


class InterventionAutocomplete(LoginPermissionRequired, autocomplete.Select2QuerySetView):
    """Provides autocomplete to search on several fields of
    :class:`~derrida.books.models.Intervention` and filter by an instance
    primary key provided by a form.

    This lets instances of :class:`~django.forms.ModelForm` that have a
    :class:`~derrida.models.Intervention` autocomplete pass a set instance
    value to restrict autocomplete results only to the Instance currently
    being edited.

    :class:`dal.autocomplete.Select2QuerySetView` allows a ``forward``
    parameter that passes JSON object as a string after as a querystring
    named ``forward``.
    :method:`dal.autocomplete.Select2QuerySetView.forwarded.get()` can
    access those variables easily.

    The autocomplete looks for an instance primary key passed with the key
    ``instance``.
    """

    permission_required = 'annotator_store.view_annotation'

    def get_queryset(self):
        interventions = Intervention.objects.all()
        if self.q:
            # Filter by quote, translations, languages, or (exact) tags
            interventions = interventions.filter(
                Q(quote__icontains=self.q) |
                Q(text__icontains=self.q) |
                Q(text_translation__icontains=self.q) |
                Q(text_language__name__icontains=self.q) |
                Q(quote_language__name__icontains=self.q) |
                Q(tags__name__in=[self.q.lower()])
            )
        instance = self.forwarded.get('instance', None)
        if instance:
            interventions = interventions.filter(
                canvas__manifest__instance__pk=instance
            )
        return interventions


class InterventionListView(ListView):
    # NOTE: adapted directly from derrida.books.views.InstanceListView
    # (probably could be generalized into a haystack faceted list view)

    model = Intervention
    form_class = InterventionSearchForm
    paginate_by = 16
    template_name = 'interventions/intervention_list.html'
    form = None
    queryset = None

    def get_queryset(self):
        sqs = SearchQuerySet().models(self.model)

        # initialize form with user search parameters and form defaults
        # preserve as QueryDict to get smart single item/list behavior
        form_opts = self.request.GET.copy()
        # set default values
        for key, val in self.form_class.defaults.items():
            # set as list to avoid nested lists
            if isinstance(val, list):
                form_opts.setlistdefault(key, val)
            else:
                form_opts.setdefault(key, val)
        self.form = self.form_class(form_opts)

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

        for facet in self.form.facet_inputs:
            # check if a value is set for this facet
            if facet in search_opts and search_opts[facet] and search_opts[facet][0]:
                solr_facet = self.form.solr_field(facet)
                # filter the query: facet matches any of the terms
                sqs = sqs.filter(**{'%s__in' % solr_facet: search_opts[facet]})

        # request range facets
        # get max/min from database to specify range start & end values
        # set the aggregate queries for this particular query and their
        # kwarg names as a dictionary
        aggregate_queries = {
            'item_work_year_max': Max('canvas__manifest__instance__work__year'),
            'item_work_year_min': Min('canvas__manifest__instance__work__year'),
            'item_copyright_year_max': Max('canvas__manifest__instance__copyright_year'),
            'item_copyright_year_min': Min('canvas__manifest__instance__copyright_year'),
            'item_print_year_max': Max('canvas__manifest__instance__print_date'),
            'item_print_year_min': Min('canvas__manifest__instance__print_date'),
        }
        # check for a namespaced _ranges variable in Django cache
        # returns None if not found by default
        ranges = cache.get('intervention_ranges')
        if not ranges:
            ranges = Intervention.objects.aggregate(**aggregate_queries)
            # pre-process datetime.date instances to get just
            # year as an integer
            for field, value in ranges.items():
                if isinstance(value, datetime.date):
                    ranges[field] = value.year
            cache.set('intervention_ranges', ranges)

        # request range facets values and optionally filter ranges
        # on configured range facet fields
        for range_facet in self.form.range_facets:
            start = end = None
            # range filter requested in search options
            if range_facet in search_opts and search_opts[range_facet]:
                start, end = search_opts[range_facet].split('-')
                # could have both start and end or just one
                # NOTE: haystack includes a range field lookup, but
                # it converts numbers to strings, so this is easier
                range_filter = '[%s TO %s]' % (start or '*', end or '*')
                sqs = sqs.filter(**{range_facet: Raw(range_filter)})

            # current range filter becomes start/end if specified
            range_opts = {
                'start': int(start) if start else ranges['%s_min' % range_facet],
                'end': int(end) if end else ranges['%s_max' % range_facet],
            }
            # calculate gap based start and end & desired number of slices
            # ideally, generate 15 slices; minimum gap size of 1
            range_opts['gap'] = max(1, int((range_opts['end'] - range_opts['start']) / 15.0))
            # restrict last range to *actual* maximum value
            range_opts['hardend'] = True
            # request the range facet with the specified options
            sqs = sqs.facet(range_facet, range=True, **range_opts)

        # sort should always be set
        if search_opts['order_by']:
            # convert sort option to corresponding solr field
            solr_sort = self.form.solr_field(search_opts['order_by'])
            # since primary sort is by book author or title,
            # always include secondary sort by annotated page
            sqs = sqs.order_by(solr_sort, 'annotated_page')

        # save for access in context data
        self.queryset = sqs
        return sqs

    def get_context_data(self, **kwargs):
        context = super(InterventionListView, self).get_context_data(**kwargs)
        facets = facet_sort_ignoreaccents(self.queryset.facet_counts(), 'item_author')
        # update multi-choice fields based on facets in the data
        self.form.set_choices_from_facets(facets.get('fields'))
        context.update({
            'facets': facets,
            'total': self.queryset.count(),
            'form': self.form,
            # specify preview image for metadata
            'page_meta_image': 'img/banner/derrida-banner-intervention-S@2x.png'
        })
        return context
