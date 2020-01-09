from unittest.mock import patch

from django.test import TestCase
from django.template.loader import get_template


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

    def test_text_template(self):
        # get an instance and corresponding reference from the fixture
        inst = Instance.objects.first()
        ref = inst.reference_set.first()
        # give reference anchor text (none in fixture)
        ref.anchor_text = 'On peut la considérer comme le développement'

        tpl = get_template('search/indexes/books/reference_text.txt')
        text = tpl.render({'object': ref})

        # no empty values should be included as text None
        assert 'None' not in text
        assert ref.derridawork.short_title in text
        assert ref.derridawork.full_citation in text
        assert ref.anchor_text in text
        # should include work title
        assert inst.work.primary_title in text
        assert inst.work.short_title in text
        assert inst.work.authors.first().firstname_last in text

        # alternate title and collected work title should be included
        coll_inst = Instance.objects.all()[1]
        inst.collected_in = coll_inst
        inst.alternate_title = 'Work in translation'
        text = tpl.render({'object': ref})
        assert inst.collected_in.display_title() in text
        assert inst.alternate_title in text
