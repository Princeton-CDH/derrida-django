"""derrida URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    # for now, since there is not yet any public-facing site,
    # redirect base url to admin index page
    url(r'^$', RedirectView.as_view(pattern_name='admin:index')),
    # # grappelli URLS for admin related lookups & autocompletes
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('pucas.cas_urls')),
]

# NOTE: for some reason this isn't getting added automatically
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += url(r'^__debug__/', include(debug_toolbar.urls)),
    except ImportError:
        pass
