from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.http import QueryDict
from django.test import TestCase
from django.urls import reverse
from haystack.query import SearchQuerySet
import pytest

from derrida.common.models import Named, Notable, DateRange
from derrida.common.utils import absolutize_url
from derrida.common.templatetags.derrida_tags import querystring_replace
from derrida.common.solr_backend import RangeSolrSearchQuery, \
    SolrRangeSearchBackend


class TestNamed(TestCase):

    def test_str(self):
        named_obj = Named(name='foo')
        assert str(named_obj) == 'foo'


class TestNotable(TestCase):

    def test_has_notes(self):
        noted = Notable()
        assert False == noted.has_notes()
        noted.notes = 'some text'
        assert True == noted.has_notes()
        noted.notes = ''
        assert False == noted.has_notes()
        noted.notes = None
        assert False == noted.has_notes()

class TestDateRange(TestCase):

    def test_dates(self):
        span = DateRange()
        # no dates set
        assert '' == span.dates
        # date range with start and end
        span.start_year = 1900
        span.end_year = 1901
        assert '1900-1901' == span.dates
        # start and end dates are same year = single year
        span.end_year = span.start_year
        assert span.start_year == span.dates
        # start date but no end
        span.end_year = None
        assert '1900-' == span.dates
        # end date but no start
        span.end_year = 1950
        span.start_year = None
        assert '-1950' == span.dates

    def test_clean_fields(self):
        with pytest.raises(ValidationError):
            DateRange(start_year=1901, end_year=1900).clean_fields()

        # should not raise exception
        # - same year is ok (single year range)
        DateRange(start_year=1901, end_year=1901).clean_fields()
        # - end after start
        DateRange(start_year=1901, end_year=1905).clean_fields()
        # - only one date set
        DateRange(start_year=1901).clean_fields()
        DateRange(end_year=1901).clean_fields()
        # exclude set
        DateRange(start_year=1901, end_year=1900).clean_fields(exclude=['start_year'])
        DateRange(start_year=1901, end_year=1900).clean_fields(exclude=['end_year'])


class TestAdminSite(TestCase):

    def setUp(self):
        # create an admin user to test autocomplete views
        self.password = 'pass!@#$'
        self.admin = get_user_model().objects.create_superuser('testadmin',
            'test@example.com', self.password)
        # staff user with minimal permissions
        self.staff = get_user_model().objects.create_user('teststafff',
            'tester@example.com', self.password, is_staff=True)

    def test_index(self):
        # admin base template customized with link to iiif digital editions
        admin_index_url = reverse('admin:index')
        # login as admin
        self.client.login(username=self.admin.username, password=self.password)
        response = self.client.get(admin_index_url)
        self.assertContains(response, reverse('djiffy:list'),
            msg_prefix='includes link to digital editions if user has perms')

        # login as staff without view_manifest permissions
        self.client.login(username=self.staff.username, password=self.password)
        response = self.client.get(admin_index_url)
        self.assertNotContains(response, reverse('djiffy:list'),
            msg_prefix='no link to digital editions if user has no perms')


def test_querystring_replace():
    mockrequest = Mock()
    mockrequest.GET = QueryDict('query=saussure')
    context = {'request': mockrequest}
    # replace when arg is not present
    args = querystring_replace(context, page=1)
    # preserves existing args
    assert 'query=saussure' in args
    # adds new arg
    assert 'page=1' in args

    mockrequest.GET = QueryDict('query=saussure&page=2')
    args = querystring_replace(context, page=3)
    assert 'query=saussure' in args
    # replaces existing arg
    assert 'page=3' in args
    assert 'page=2' not in args

    # handle repeating terms
    mockrequest.GET = QueryDict('language=english&language=french')
    args = querystring_replace(context, page=10)
    assert 'language=english' in args
    assert 'language=french' in args
    assert 'page=10' in args


@pytest.mark.django_db
def test_absolutize_url():
    https_url = 'https://example.com/some/path/'
    # https url is returned unchanged
    assert absolutize_url(https_url) == https_url
    # testing with default site domain
    current_site = Site.objects.get_current()

    # test site domain without https
    current_site.domain = 'example.org'
    current_site.save()
    local_path = '/foo/bar/'
    assert absolutize_url(local_path) == 'https://example.org/foo/bar/'
    # trailing slash in domain doesn't result in double slash
    current_site.domain = 'example.org/'
    current_site.save()
    assert absolutize_url(local_path) == 'https://example.org/foo/bar/'
    # site at subdomain should work too
    current_site.domain = 'example.org/sub/'
    current_site.save()
    assert absolutize_url(local_path) == 'https://example.org/sub/foo/bar/'
    # site with https:// included
    current_site.domain = 'https://example.org'
    assert absolutize_url(local_path) == 'https://example.org/sub/foo/bar/'


class TestRangeSolrEngine(object):

    # this depends on local/test settings, but flagging here might
    # actually be helpful
    def test_config(self):
        sqs = SearchQuerySet()
        assert isinstance(sqs.query, RangeSolrSearchQuery)
        assert isinstance(sqs.query.backend, SolrRangeSearchBackend)

    def test_add_range_facet(self):
        # normal facet shouldn't set range facet
        sqs = SearchQuerySet().facet('title_exact')
        assert not sqs.query.range_facets

        range_field = 'publication_date'
        opts = {'start': 1, 'end': 100, 'gap': 10, 'range': True}
        sqs = SearchQuerySet().facet(range_field, **opts)
        assert range_field in sqs.query.range_facets
        assert sqs.query.range_facets[range_field] == opts

    def test_build_range_facet_params(self):
        # no range facet
        sqs = SearchQuerySet()
        params = sqs.query.build_params()
        assert 'facet.range' not in params

        # with range facet
        range_field = 'publication_date'
        opts = {'start': 1, 'end': 100, 'gap': 10, 'range': True}
        sqs = SearchQuerySet().facet(range_field, **opts)
        params = sqs.query.build_params()
        assert params['facet.range'] == [range_field]
        assert params['f.publication_date.facet.range.start'] == opts['start']
        assert params['f.publication_date.facet.range.end'] == opts['end']
        assert params['f.publication_date.facet.range.gap'] == opts['gap']

    def test_clone(self):
        # with range facet
        range_field = 'publication_date'
        opts = {'start': 1, 'end': 100, 'gap': 10, 'range': True}
        sqs = SearchQuerySet().facet(range_field, **opts)
        cloned_sqs = sqs._clone()
        # preserves range facets and query subclass
        assert cloned_sqs.query.range_facets == sqs.query.range_facets
        assert isinstance(cloned_sqs.query, RangeSolrSearchQuery)

    def test_post_process_facets(self):
        # sample facet range response
        result = {
            'facets': {},
            'facet_ranges': [
                {'print_year':
                    {'counts': ['1954', 1, '1955', 0, '1956', 5, '1957', 0, '1958', 0, '1959', 0, '1960', 0, '1961', 0, '1962', 10, '1963', 0],
                    'gap': 1, 'end': 1964, 'start': 1954},
                },
            ]
        }
        sqs = SearchQuerySet()
        facets = sqs.query.post_process_facets(result)
        assert 'ranges' in facets
        assert facets['ranges']['print_year']
        # flat list converted into turn-flat-list-into-two-tuples
        assert facets['ranges']['print_year']['counts'][0] == ('1954', 1)
        for range_field in ['gap', 'end', 'start']:
            assert range_field in facets['ranges']['print_year']
        assert facets['ranges']['print_year']['max'] == 10

