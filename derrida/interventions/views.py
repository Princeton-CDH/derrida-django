from dal import autocomplete
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import PermissionRequiredMixin
from djiffy import views as djiffy_views

from .models import Tag


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


class CanvasAutocomplete(LoginPermissionRequired, djiffy_views.CanvasAutocomplete):
    permission_required = 'djiffy.view_canvas'
