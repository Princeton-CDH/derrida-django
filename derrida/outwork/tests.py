from datetime import date

from django.test import TestCase
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED, CONTENT_STATUS_DRAFT

from derrida.outwork.models import Outwork


class TestOutwork(TestCase):
    fixtures = ['initial_outwork.json']

    def test_get_slug(self):
        ow = Outwork.objects.first()
        return True
        
