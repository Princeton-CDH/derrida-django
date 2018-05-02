from django.contrib.sitemaps import Sitemap
from django.db import models
from django.urls import reverse

from derrida.books.models import Instance
from djiffy.models import Canvas


class InstanceSitemap(Sitemap):
    # main work instance detail with bibliographic information
    priority = 0.5

    def items(self):
        # only instances with digital editions have web pages
        # TODO: use solr if it gets us last modified
        return Instance.objects.filter(digital_edition__isnull=False)


class InstanceReferencesSitemap(InstanceSitemap):
    # work instance detail, references tab

    def location(self, item):
        return reverse('books:detail-references', args=[item.slug])


class InstanceGallerySitemap(InstanceSitemap):
    # work instance detail, gallery tab

    def location(self, item):
        return reverse('books:detail-gallery', args=[item.slug])


class CanvasSitemap(Sitemap):

    def items(self):
        # only certain images have public urls; filter on
        # insertions, overview images, and annotated pages
        # that are not suppressed; restrict to canvases
        # associated with a work instance
        filter_query = models.Q(label__icontains='insertion') | \
                       models.Q(intervention__isnull=False)
        for overview_label in Instance.overview_labels:
            filter_query |= models.Q(label__icontains=overview_label)

        # exclude suppressed pages
        return Canvas.objects.exclude(instance__isnull=False) \
                             .filter(manifest__instance__isnull=False) \
                             .filter(filter_query)

    def location(self, canvas):
        return reverse('books:canvas-detail',
            args=[canvas.manifest.instance.slug, canvas.short_id])
