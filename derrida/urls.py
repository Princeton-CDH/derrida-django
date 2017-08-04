"""derrida URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from annotator_store import views as annotator_views

urlpatterns = [
    # for now, since there is not yet any public-facing site,
    # redirect base url to admin index page
    url(r'^$', RedirectView.as_view(pattern_name='admin:index'), name='site-index'),

    # placeholders for new design
    url(r'^citations/$', RedirectView.as_view(pattern_name='admin:index'), name='citations-list'),

    # grappelli URLS for admin related lookups & autocompletes
    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('pucas.cas_urls')),
    url(r'^library/', include('derrida.books.urls', namespace='books')),
    url(r'^people/', include('derrida.people.urls', namespace='people')),
    url(r'^places/', include('derrida.places.urls', namespace='places')),
    url(r'^interventions/', include('derrida.interventions.urls', namespace='interventions')),

    # local version of djiffy urls
    url(r'^admin/iiif-books/', include('derrida.interventions.iiif_urls', namespace='djiffy')),

    # annotations API
    url(r'^annotations/api/', include('annotator_store.urls', namespace='annotation-api')),

    # annotatorjs doesn't handle trailing slash in api prefix url
    url(r'^annotations/api', annotator_views.AnnotationIndex.as_view(), name='annotation-api-prefix'),

    url(r'^index', TemplateView.as_view(template_name='public/index.html'), name="home"),
    # url(r'^library', TemplateView.as_view(template_name='public/library.html'), name="library"),
    # url(r'^visualization', TemplateView.as_view(template_name='public/visualization.html'), name="visualization"),

    # url(r'^book/bibliography', TemplateView.as_view(template_name='public/item/bibliography.html'), name="bibliography"),
    # url(r'^book/image-gallery', TemplateView.as_view(template_name='public/item/image-gallery.html'), name="image-gallery"),
    # url(r'^book/citation-view', TemplateView.as_view(template_name='public/item/citation-list.html'), name="citation-view"),
    # url(r'^book', TemplateView.as_view(template_name='public/item/bibliography.html'), name="book"),

    url(r'^citations', TemplateView.as_view(template_name='public/citations.html'), name="citations-list"),
]

# NOTE: for some reason this isn't getting added automatically
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += url(r'^__debug__/', include(debug_toolbar.urls)),
    except ImportError:
        pass
