from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from derrida.interventions.views import TagAutocomplete


urlpatterns = [
    url(r'^tags/autocomplete/$',
        staff_member_required(TagAutocomplete.as_view()), name='tag-autocomplete'),
    url(r'^tags/(?P<mode>(annotation|insertion))/autocomplete/$',
        staff_member_required(TagAutocomplete.as_view()), name='tag-autocomplete'),
]
