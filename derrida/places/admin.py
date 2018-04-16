from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from dal import autocomplete

from .models import Place


class GeonamesLookupWidget(autocomplete.Select2):
    '''Customize autocomplete select widget to display Geonames URI
    as a link and render a map for the selected location.'''
    # (inspired by )

    def render(self, name, value, attrs=None):
        # select2 filters based on existing choices (non-existent here),
        # so when a value is set, add it to the list of choices
        if value:
            self.choices = [(value, value)]
        widget = super(GeonamesLookupWidget, self).render(name, value, attrs)
        return mark_safe((u'<div id="geonames_map"></div>' +
            u'%s<p><a id="geonames_uri" target="_blank" href="%s">%s</a></p>') % \
            (widget, value or '', value or ''))


class PlaceAdminForm(forms.ModelForm):
    '''Custom model form for Place editing, used to add geonames lookup.'''

    #: add a hidden field to pass in a mapbox access token from local settings
    mapbox_token = forms.CharField(initial=getattr(settings, 'MAPBOX_ACCESS_TOKEN', ''),
        widget=forms.HiddenInput)

    class Meta:
        model = Place
        exclude = []
        widgets = {
            'geonames_id': GeonamesLookupWidget(url='places:geonames-autocomplete',
                attrs={'data-placeholder': 'Type location name to search...',
                       'data-minimum-input-length': 3})
        }


class PlaceAdmin(admin.ModelAdmin):
    form = PlaceAdminForm
    list_display = ('name', 'geonames_id', 'has_notes')
    fields = ('name', 'geonames_id', 'latitude', 'longitude', 'notes',
        'mapbox_token')
    search_fields = ('name', 'notes', 'geonames_id')
    class Media:
        static_url = getattr(settings, 'STATIC_URL')
        css = {
            'all': ['https://unpkg.com/leaflet@1.0.2/dist/leaflet.css',
                    'admin/geonames.css']
        }
        js = ['admin/geonames-lookup.js',
            'https://unpkg.com/leaflet@1.0.2/dist/leaflet.js']

admin.site.register(Place, PlaceAdmin)
