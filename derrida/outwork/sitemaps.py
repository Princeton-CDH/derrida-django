from django.contrib.sitemaps import Sitemap

from mezzanine.pages.models import Page


class PageSitemap(Sitemap):
    # sitemap for mezzanine pages; includes top-level dynamic pages
    default_priority = 0.5

    def items(self):
        # only instances with digital editions have web pages
        return Page.objects.published().filter(in_sitemap=True)

    lastmod_slugs = ['library', 'interventions', 'outwork']

    def lastmod(self, item):
        # last modified information currently not available for db content
        # don't return page modified, since it is inaccurate
        if item.slug in self.lastmod_slugs or item.slug.startswith('references'):
            return None
        return item.updated

    def priority(self, item):
        # primary menu
        if '1' in item.in_menus:
            return 0.7
        # footer menu
        if '3' in item.in_menus:
            return 0.6
        return self.default_priority

