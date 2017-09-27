'''Tests for utility functions for Derrida'''
from derrida.utils import deligature
from django.test import TestCase


def test_deligature():
    '''Check that deligature removes unicode Latin ligatures'''
    ligatured = 'Œ œ Æ æ'
    assert deligature(ligatured) == 'Oe oe Ae ae'


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
