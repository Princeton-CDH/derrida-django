'''Tests for utility functions for Derrida'''
from unittest.mock import Mock, patch

from django.conf import settings
from django.test import TestCase, override_settings
from derrida.context_processors import template_settings

class TestRobotsTxt(TestCase):

    def test_robots_txt(self):
        res = self.client.get('/robots.txt')
        # successfully gets robots.txt
        assert res.status_code == 200
        # is text/plain
        assert res['Content-Type'] == 'text/plain'
        # uses robots.txt template
        assert 'robots.txt' in [template.name for template in res.templates]
        with self.settings(DEBUG=False):
            res = self.client.get('/robots.txt')
            self.assertContains(res, 'Disallow: /admin')
        with self.settings(DEBUG=True):
            res = self.client.get('/robots.txt')
            self.assertContains(res, 'Disallow: /')


class TestContextProcessors(TestCase):

    @override_settings()
    @patch('derrida.context_processors.SearchForm')
    def test_template_settings(self, mockform):
        mockrequest = Mock()
        # empty GET request
        mockrequest.GET.return_value = {}
        del settings.SHOW_TEST_WARNING
        del settings.INCLUDE_ANALYTICS
        context_extras = template_settings(mockrequest)

        # check that everything was called with the right defaults given
        # no settings
        assert isinstance(context_extras, dict)
        assert not context_extras['SHOW_TEST_WARNING']
        assert not context_extras['INCLUDE_ANALYTICS']
        mockform.assert_called_with(mockrequest.GET)
        assert context_extras['search_form'] == mockform()
        # check that settings are passed as expected too
        with self.settings(
            SHOW_TEST_WARNING=True,
            INCLUDE_ANALYTICS=True
        ):
            context_extras = template_settings(mockrequest)
            assert context_extras['SHOW_TEST_WARNING']
            assert context_extras['INCLUDE_ANALYTICS']
            assert context_extras['search_form'] == mockform()

    def test_templates(self):

        with self.settings(
            SHOW_TEST_WARNING=True,
            INCLUDE_ANALYTICS=True
        ):
            response = self.client.get('/')
            print(response.render().content)
            self.assertContains(response, '<div class="ribbon-box fade">')
