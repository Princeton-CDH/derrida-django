from django.test import TestCase
from django.utils.timezone import now
from mezzanine.core.models import (CONTENT_STATUS_DRAFT,
                                   CONTENT_STATUS_PUBLISHED)
from mezzanine.pages.models import Page
from mezzanine.utils.urls import slugify

from derrida.outwork.models import Outwork


class TestOutwork(TestCase):
    fixtures = ['initial_outwork.json']

    @classmethod
    def setUpTestData(cls):
        cls.culture = Outwork.objects.get(pk=10) # 'Culture et écriture' essay outwork
        cls.outwork = Page.objects.get(title="Outwork") # main Outwork page

    def test_repr(self):
        assert repr(self.culture) == '<Outwork: {}>'.format(self.culture.slug)

    def test_get_slug(self):
        year = now().year
        title = slugify(self.culture.title)
        # should use year created if not yet published
        self.culture.publish_date = None
        assert 'outwork/{}/'.format(self.culture.created.year) in self.culture.get_slug()
        # should use year published if published
        self.culture.publish_date = now()
        assert 'outwork/{}/'.format(year) in self.culture.get_slug()
        # should have 'outwork' exactly once in the slug
        self.culture.parent = None
        assert self.culture.get_slug() == 'outwork/{}/{}'.format(year, title)
        # even if it's a child of the main outwork page
        self.culture.parent = self.outwork
        assert self.culture.get_slug() == 'outwork/{}/{}'.format(year, title)

    def test_is_published(self):
        # false if draft
        self.culture.status = CONTENT_STATUS_DRAFT
        self.culture.save()
        assert self.culture.is_published() is False
        # true if published
        self.culture.status = CONTENT_STATUS_PUBLISHED
        self.culture.save()
        assert self.culture.is_published() is True
