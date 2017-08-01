from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
import pytest

from .models import Named, Notable, DateRange

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





