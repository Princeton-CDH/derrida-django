from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from derrida.interventions import views


urlpatterns = [
    url(r'^$', views.InterventionListView.as_view(), name='list'),
    url(r'^tags/autocomplete/$',
        staff_member_required(views.TagAutocomplete.as_view()), name='tag-autocomplete'),
    url(r'^tags/(?P<mode>(annotation|insertion))/autocomplete/$',
        staff_member_required(views.TagAutocomplete.as_view()), name='tag-autocomplete'),
    url(r'^interventions/autocomplete/$',
        views.InterventionAutocomplete.as_view(), name='autocomplete')
]
