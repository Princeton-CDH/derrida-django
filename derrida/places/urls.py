from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from derrida.places.views import PlaceAutocomplete, GeonamesLookup


app_name = 'derrida.places'

urlpatterns = [
    url(r'^autocomplete/$', staff_member_required(PlaceAutocomplete.as_view()),
        name='autocomplete'),
    url(r'^autocomplete/geonames/$',
        staff_member_required(GeonamesLookup.as_view()),
         name='geonames-autocomplete')
]
