from django.test import TestCase
from django.urls import reverse
from djiffy.models import Canvas

from derrida.books import sitemaps as book_sitemaps
from derrida.books.models import Instance


class TestInstanceSitemap(TestCase):
    fixtures = ['test_instances']

    def test_items(self):
        sitemap_items = book_sitemaps.InstanceSitemap().items()
        # should not include items without digital edition
        assert Instance.objects.filter(digital_edition__isnull=True).first() \
            not in sitemap_items
        # should include items with digital edition
        assert Instance.objects.filter(digital_edition__isnull=False).first() \
            in sitemap_items


class TestInstanceReferencesSitemap(TestCase):
    fixtures = ['test_instances']

    def test_location(self):
        item = Instance.objects.filter(digital_edition__isnull=False).first()
        assert book_sitemaps.InstanceReferencesSitemap().location(item) == \
            reverse('books:detail-references', args=[item.slug])


class TestInstanceGallerySitemap(TestCase):
    fixtures = ['test_instances']

    def test_location(self):
        item = Instance.objects.filter(digital_edition__isnull=False).first()
        assert book_sitemaps.InstanceGallerySitemap().location(item) == \
            reverse('books:detail-gallery', args=[item.slug])


class TestCanvasSitemap(TestCase):
    fixtures = ['test_interventions']

    def test_items(self):
        sitemap_items = book_sitemaps.CanvasSitemap().items()
        # should include insertions and overview labels

        # should include canvas with associated intervention
        intervention = Canvas.objects.filter(intervention__isnull=False) \
                             .first()
        assert intervention in sitemap_items

        # should not include canvas without associated intervention
        assert Canvas.objects.filter(intervention__isnull=True).first() \
            not in sitemap_items

        # create test cover & insertion to test inclusion
        manifest = Canvas.objects.first().manifest
        cover = Canvas.objects.create(manifest=manifest, label='cover',
                                      order=100, short_id='cover')
        insertion = Canvas.objects.create(manifest=manifest,
                                          label='insertion a',
                                          order=101, short_id='insert-a')
        # get fresh set of items to test
        sitemap_items = book_sitemaps.CanvasSitemap().items()
        assert cover in sitemap_items
        assert insertion in sitemap_items

        # suppressed pages should be excluded
        instance = intervention.manifest.instance
        # - suppress single page
        instance.suppressed_images.add(intervention)
        assert intervention not in book_sitemaps.CanvasSitemap().items()
        # - suppress all images
        instance.suppressed_images.remove(intervention)
        instance.suppress_all_images = True
        instance.save()
        assert intervention not in book_sitemaps.CanvasSitemap().items()

        # # exclude suppressed pages
        # return Canvas.objects.exclude(instance__isnull=False) \
        #                      .filter(manifest__instance__isnull=False) \
        #                      .filter(filter_query)

    def test_location(self):
        item = Canvas.objects.first()
        assert book_sitemaps.CanvasSitemap().location(item) == \
            reverse('books:canvas-detail',
                    args=[item.manifest.instance.slug, item.short_id])
