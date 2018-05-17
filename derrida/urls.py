"""derrida URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
"""
from annotator_store import views as annotator_views
# from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
import mezzanine.urls
import mezzanine.pages.views

from derrida.books.views import SearchView
from derrida.books import sitemaps as book_sitemaps
from derrida.outwork import sitemaps as page_sitemaps


sitemaps = {
    'pages': page_sitemaps.PageSitemap,
    'books': book_sitemaps.InstanceSitemap,
    'book-references': book_sitemaps.InstanceReferencesSitemap,
    'book-gallery': book_sitemaps.InstanceGallerySitemap,
    'book-pages': book_sitemaps.CanvasSitemap,
}


urlpatterns = [

     url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
        content_type='text/plain')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico',
        permanent=True)),
    url(r'^sitemap\.xml$', sitemap_views.index, {'sitemaps': sitemaps},
        name='sitemap-index'),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap_views.sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

    # home page managed via mezzanine, but needs a named url
    url(r'^$', mezzanine.pages.views.page, {"slug": "/"}, name="home"),
    # alternate homepage named url needed for djiffy templates
    url(r'^$', mezzanine.pages.views.page, {"slug": "/"}, name="site-index"),

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

    # content pages managed by mezzanine
    url("^", include(mezzanine.urls))
]


# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
