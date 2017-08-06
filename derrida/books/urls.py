from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from derrida.books import views


urlpatterns = [
    # TODO: come up with cleaner url patterns/names for autocomplete views
    url(r'^publishers/autocomplete/$', staff_member_required(views.PublisherAutocomplete.as_view()),
        name='publisher-autocomplete'),
    url(r'^languages/autocomplete/$', staff_member_required(views.LanguageAutocomplete.as_view()),
        name='language-autocomplete'),
    url(r'^library/$', views.InstanceListView.as_view(), name='list'),
    url(r'^library/(?P<pk>\d+)/$', views.InstanceDetailView.as_view(), name='detail'),
    url(r'^references/$', views.ReferenceListView.as_view(), name='reference-list'),
    url(r'^references/histogram/$', views.ReferenceHistogramView.as_view(),
        name='reference-histogram'),
]
