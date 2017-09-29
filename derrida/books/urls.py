from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from derrida.books import views



urlpatterns = [
    url(r'^publishers/autocomplete/$', staff_member_required(views.PublisherAutocomplete.as_view()),
        name='publisher-autocomplete'),
    url(r'^languages/autocomplete/$', staff_member_required(views.LanguageAutocomplete.as_view()),
        name='language-autocomplete'),

    # cross-item search
    url(r'^search/$', views.SearchView.as_view(), name='search'),

    url(r'^references/$', views.ReferenceListView.as_view(), name='reference-list'),
    url(r'^references/histogram/$', views.ReferenceHistogramView.as_view(),
        name='reference-histogram'),
    url(r'^references/histogram/(?P<derridawork_slug>[a-z-]+)/$',
        views.ReferenceHistogramView.as_view(), {'mode': 'section'},
        name='reference-histogram'),
    url(r'^references/(?P<derridawork_slug>[a-z-]+)/(?P<page>[\dA-Z]+)(?P<pageloc>[a-z]+)?/$',
        views.ReferenceDetailView.as_view(), name='reference'),

    url(r'^library/$', views.InstanceListView.as_view(), name='list'),
    url(r'^library/(?P<slug>[-\w]+)/$', views.InstanceDetailView.as_view(), name='detail'),
    url(r'^library/(?P<slug>[-\w]+)/gallery/$',
        views.InstanceDetailView.as_view(template_name='books/detail/gallery.html'),
        name='detail-gallery'),
    url(r'^library/(?P<slug>[-\w]+)/citations/$',
        views.InstanceReferenceDetailView.as_view(), name='detail-citations'),

    url(r'^library/(?P<slug>[-\w]+)/gallery/(?P<short_id>[a-z0-9]+)/$',
        views.CanvasDetail.as_view(), name='canvas-detail'),
    # canvas image views
    url(r'^library/(?P<slug>[-\w]+)/gallery/images/(?P<page_num>[0-9]{1,4})-?[0-9]*[a-z]?/$',
        views.CanvasImageByPageNumber.as_view(), {'mode': 'by-page'}, name='canvas-by-page'),
    url(r'^library/(?P<slug>[-\w]+)/gallery/images/(?P<short_id>[a-z0-9]+)/(?P<mode>thumbnail|large)/$',
        views.CanvasImage.as_view(), name='canvas-image'),

    # default thumbnail for a book
    url(r'^library/(?P<slug>[-\w]+)/images/thumbnail/$',
        views.CanvasImage.as_view(), {'mode': 'thumbnail'}, name='book-thumbnail')

]
