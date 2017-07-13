import json

from dal import autocomplete
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from djiffy import views as djiffy_views

from derrida.books.models import Instance, Language
from derrida.interventions.models import Intervention
from .models import Tag, get_default_intervener


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
        languages = Language.objects.all().values_list('name', flat=True)
        context['languages_js'] = json.dumps(list(languages))
        # pass in default authorized name for Derrida, if he exists, else a
        # literal '' for annotator_init.html
        derrida = get_default_intervener()
        context['default_intervener'] = json.dumps('')
        if derrida:
            context['default_intervener'] = json.dumps(derrida.authorized_name)
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
