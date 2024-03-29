from django.conf.urls import url, include
from django.contrib.admin.views.decorators import staff_member_required

from derrida.books import views


app_name = 'derrida.books'

urlpatterns = [
    url(r'^publishers/autocomplete/$', staff_member_required(views.PublisherAutocomplete.as_view()),
        name='publisher-autocomplete'),
    url(r'^languages/autocomplete/$', staff_member_required(views.LanguageAutocomplete.as_view()),
        name='language-autocomplete'),

    # cross-item search
    url(r'^search/$', views.SearchView.as_view(), name='search'),

    # reference views
    url(r'^references/', include([
        url(r'^$', views.ReferenceListView.as_view(), name='reference-list'),
        url(r'^histogram/$', views.ReferenceHistogramView.as_view(),
            name='reference-histogram'),
        url(r'^histogram/(?P<derridawork_slug>[a-z-\d]+)/$',
            views.ReferenceHistogramView.as_view(), {'mode': 'section'},
            name='reference-histogram'),
        url(r'^(?P<derridawork_slug>[a-z-]+)/(?P<page>[\dA-Z]+)(?P<pageloc>[a-z]+)?/$',
            views.ReferenceDetailView.as_view(), name='reference'),
    ])),

    # library views
    url(r'^library/', include([
        url(r'^$', views.InstanceListView.as_view(), name='list'),
        url(r'^(?P<slug>[-\w]+)/', include([
            url(r'^$', views.InstanceDetailView.as_view(), name='detail'),
            url(r'^references/$',
                views.InstanceReferenceDetailView.as_view(), name='detail-references'),
            url(r'^gallery/$',
                views.InstanceDetailView.as_view(template_name='books/detail/gallery.html'),
                name='detail-gallery'),
            url(r'^gallery/(?P<short_id>[a-z0-9-]+)/$',
                views.CanvasDetail.as_view(), name='canvas-detail'),
            url(r'^suppress-images/$', views.CanvasSuppress.as_view(), name='suppress-canvas'),
            # canvas image views
            url(r'^gallery/images/(?P<page_num>[0-9vix]{1,4})-?[0-9]*[a-z]?(?P<x>@2x)?/$',
                views.CanvasImageByPageNumber.as_view(), {'mode': 'by-page'}, name='canvas-by-page'),
            url(r'^gallery/images/(?P<short_id>[a-z0-9-]+|default)/(?P<mode>smthumb|thumbnail|large|info)(?P<x>@2x)?/$',
                views.CanvasImage.as_view(), name='canvas-image'),
            url(r'^gallery/images/(?P<short_id>[a-z0-9-]+)/(?P<mode>iiif)(?P<url>.*)$',
                views.CanvasImage.as_view(), name='canvas-iiif'),

            # default thumbnail for a book
            url(r'^(?P<mode>smthumb|thumbnail)(?P<x>@2x)?/$',
                views.CanvasImage.as_view(), name='book-image')
        ])) # end library/<slug> urls
    ])), # end library urls

    url(r'^titles/(?P<pk>\d+)/', views.InstanceURIView.as_view(), name='instance'),

]
