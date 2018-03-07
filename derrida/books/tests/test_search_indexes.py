from unittest.mock import patch
from django.test import TestCase
from derrida.books.models import Reference, Instance
from derrida.books.search_indexes import ReferenceIndex


class TestReferenceIndex(TestCase):
    fixtures = ['test_references.json']

    def setUp(self):
        '''None of the Instacefixtures have slugs, so generate them'''
        for instance in Instance.objects.all():
            instance.slug = instance.generate_safe_slug()
            instance.save()

        self.refindex = ReferenceIndex()

    def test_prepare_book_page_sort(self):
        refindex = self.refindex

        # sample reference book pages values with expected sort value
        page_values = [('', 0), ('62p', 62), ('44s', 44), ('v', -495),
            ('38', 38), ('(452a)47p', 47), ('22-23', 22), ('L', -450),
            ('___(chapter VI)', 0), ('10-11', 10), ('105-111', 105)]

        for input_val, expected_val in page_values:
            ref = Reference(book_page=input_val)
            assert refindex.prepare_book_page_sort(ref) == expected_val

