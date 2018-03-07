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

    def test_prepare_instance_slug(self):

        # get a ReferenceIndex object
        refindex = self.refindex
        # get a reference
        reference = Reference.objects.first()
        # not a book section (none in test set are)
        # should return the slug of its instance
        slug = refindex.prepare_instance_slug(reference)
        assert slug == reference.instance.slug

        # create a work as a 'collected in'
        ecrit = Instance.objects.get(slug__icontains='lecriture-et-la')
        debat = Instance.objects.get(slug__icontains='le-debat-sur')
        # make ecrit a 'section' of debat
        ecrit.collected_in = debat
        ecrit.save()
        # get a reference from ecrit
        reference = Reference.objects.filter(instance=ecrit).first()
        # should return the slug for debat not ecrit
        slug = refindex.prepare_instance_slug(reference)
        assert slug == debat.slug

    def test_prepare_book_page_sort(self):
        refindex = self.refindex

        # sample reference book pages values with expected sort value
        page_values = [('', 0), ('62p', 62), ('44s', 44), ('v', -495),
            ('38', 38), ('(452a)47p', 47), ('22-23', 22), ('L', -450),
            ('___(chapter VI)', 0)]

        for input_val, expected_val in page_values:
            ref = Reference(book_page=input_val)
            assert refindex.prepare_book_page_sort(ref) == expected_val

