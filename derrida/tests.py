'''Tests for utility functions for Derrida'''
from django.test import TestCase


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
