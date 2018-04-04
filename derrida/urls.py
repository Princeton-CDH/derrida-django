"""derrida URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
"""
from annotator_store import views as annotator_views
# from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
import mezzanine.urls
import mezzanine.pages.views

from derrida.books.views import SearchView


urlpatterns = [
    # error pages - remove after testing
    url(r'^404/$', mezzanine.core.views.page_not_found, ),
    url(r'^500/$', mezzanine.core.views.server_error, ),

     url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
        content_type='text/plain')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico',
        permanent=True)),

    # home page managed via mezzanine, but needs a named url
    url(r'^$', mezzanine.pages.views.page, {"slug": "/"}, name="home"),
    # alternate homepage named url needed for djiffy templates
    url(r'^$', mezzanine.pages.views.page, {"slug": "/"}, name="site-index"),

    # placeholders for new design
    url(r'^citations/$', RedirectView.as_view(pattern_name='admin:index'), name='citations-list'),

    # grappelli URLS for admin related lookups & autocompletes
    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('pucas.cas_urls')),
    url(r'^', include('derrida.books.urls', namespace='books')),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^people/', include('derrida.people.urls', namespace='people')),
    url(r'^places/', include('derrida.places.urls', namespace='places')),
    url(r'^interventions/', include('derrida.interventions.urls', namespace='interventions')),
    url(r'^viaf/', include('viapy.urls', namespace='viaf')),
    url(r'^outwork/', include('derrida.outwork.urls', namespace='outwork')),

    # local version of djiffy urls
    url(r'^admin/iiif-books/', include('derrida.interventions.iiif_urls', namespace='djiffy')),

    # annotations API
    url(r'^annotations/api/', include('annotator_store.urls', namespace='annotation-api')),

    # annotatorjs doesn't handle trailing slash in api prefix url
    url(r'^annotations/api', annotator_views.AnnotationIndex.as_view(), name='annotation-api-prefix'),

    # url(r'^library', TemplateView.as_view(template_name='public/library.html'), name="library"),
    url(r'^visualization', TemplateView.as_view(template_name='public/visualization.html'), name="visualization"),

    url(r'^citations', TemplateView.as_view(template_name='public/citations.html'), name="citations-list"),

    # url(r'^search', TemplateView.as_view(template_name='public/search-results.html'), name="search"),

    url(r'^inputs', TemplateView.as_view(template_name='public/search-inputs.html'), name="show-inputs"),

    # content pages managed by mezzanine
    url("^", include(mezzanine.urls))
]


# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
