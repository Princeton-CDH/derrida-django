from django.conf.urls import url

from .views import ManifestList, ManifestDetail, CanvasDetail, \
    CanvasAutocomplete

# override the default djiffy views to require view permissions
# in order to access to digitized content

urlpatterns = [
    url(r'^$', ManifestList.as_view(), name='list'),
    url(r'^(?P<id>[^/]+)/$', ManifestDetail.as_view(), name='manifest'),
    url(r'^(?P<manifest_id>[^/]+)/canvases/(?P<id>[^/]+)/$',
        CanvasDetail.as_view(), name='canvas'),
    url(r'^canvas/autocomplete/$', CanvasAutocomplete.as_view(),
        name='canvas-autocomplete'),
]
