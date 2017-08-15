from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from derrida.books import views



urlpatterns = [
    # TODO: come up with cleaner url patterns/names for autocomplete views
    url(r'^publishers/autocomplete/$', staff_member_required(views.PublisherAutocomplete.as_view()),
        name='publisher-autocomplete'),
    url(r'^languages/autocomplete/$', staff_member_required(views.LanguageAutocomplete.as_view()),
        name='language-autocomplete'),

    url(r'^references/$', views.ReferenceListView.as_view(), name='reference-list'),
    url(r'^references/histogram/$', views.ReferenceHistogramView.as_view(),
        name='reference-histogram'),
    url(r'^references/histogram/(?P<derridawork_abbrev>[a-z]+)/$',
        views.ReferenceHistogramView.as_view(), {'mode': 'section'},
        name='reference-histogram'),

    url(r'^references/(?P<derridawork_abbrev>[a-z]+)(?P<page>[\dA-Z]+)(?P<pageloc>[a-z]+)?/$',
        views.ReferenceDetailView.as_view(), name='reference'),

    url(r'^library/$', views.InstanceListView.as_view(), name='list'),
    url(r'^library/(?P<pk>\d+)/$', views.InstanceDetailView.as_view(), name='detail'),
    url(r'^library/(?P<pk>\d+)/gallery/$',
        views.InstanceDetailView.as_view(template_name='books/detail/gallery.html'),
        name='detail-gallery'),
    url(r'^library/(?P<pk>\d+)/citations/$',
        views.InstanceDetailView.as_view(template_name='books/detail/citations.html'),
        name='detail-citations'),
]
