from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
from haystack.models import SearchResult
from mezzanine.core.models import (CONTENT_STATUS_DRAFT,
                                   CONTENT_STATUS_PUBLISHED)
from mezzanine.pages.models import Page
from mezzanine.utils.urls import slugify
import pytest

from derrida.books.tests.test_views import USE_TEST_HAYSTACK
from derrida.outwork.models import Outwork


class TestOutwork(TestCase):
    fixtures = ['initial_outwork']

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


@USE_TEST_HAYSTACK
class TestOutworkViews(TestCase):
    fixtures = ['initial_outwork']

    @pytest.mark.haystack
    def test_outwork_list(self):
        outwork_list_url = reverse('outwork:list')
        response = self.client.get(outwork_list_url)
        assert response.status_code == 200
        assert 'object_list' in response.context
        assert isinstance(response.context['object_list'][0], SearchResult)
        assert response.context['object_list'][0].model == Outwork
        self.assertTemplateUsed(response, 'outwork/outwork_list.html')
        self.assertTemplateUsed(response, 'outwork/components/outwork-list-item.html')
        # not enough items to paginate
        self.assertTemplateNotUsed(response, 'components/page-pagination.html')

        # outwork summary details that should be present in the template
        outwork = Outwork.objects.first()
        # spot check template (tested more thoroughly in reference detail below)
        self.assertContains(response, outwork.title,
            msg_prefix='outwork list should display outwork essay title')
        self.assertContains(response, outwork.get_absolute_url(),
            msg_prefix='outwork list should link to essay')

        # keyword search with no match
        response = self.client.get(outwork_list_url, {'query': 'foo'})
        self.assertTemplateUsed(response, 'components/search-results-empty.html')
