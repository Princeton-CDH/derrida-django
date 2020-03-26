from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from derrida.interventions import views
from derrida.interventions.models import Intervention


app_name = 'derrida.interventions'

urlpatterns = [
    url(r'^$', views.InterventionListView.as_view(), name='list'),
    url(r'^tags/autocomplete/$',
        staff_member_required(views.TagAutocomplete.as_view()), name='tag-autocomplete'),
    url(r'^tags/(?P<mode>(annotation|insertion))/autocomplete/$',
        staff_member_required(views.TagAutocomplete.as_view()), name='tag-autocomplete'),
    url(r'^autocomplete/$',
        views.InterventionAutocomplete.as_view(), name='autocomplete'),
    url(r'^(?P<id>%s)/$' % Intervention.UUID_REGEX,
        views.InterventionView.as_view(), name='view'),
]
