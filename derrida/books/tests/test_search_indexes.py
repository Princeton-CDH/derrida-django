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
        # get all references by pk
        references = Reference.objects.all().order_by('pk')
        expected_book_pages = [
            0, 0, 0, 0, 62, 171, 0, 87, 87, 44, 126, 148, 355, -495, 23, 256,
            0, 38, 43, 0
        ]
        i = 0
        # check that each one's page number is convered to an integer
        # as expected
        for reference in references:
            integered = refindex.prepare_book_page_sort(reference)
            assert expected_book_pages[i] == integered
            i += 1
        # check a few variant patterns
        reference = Reference.objects.first()
        # page includes back reference
        reference.book_page = '(452a)47p'
        # should be just 47
        assert refindex.prepare_book_page_sort(reference) == 47
        # page is a chapter or something we simply can't guess at
        reference.book_page = '___(chapter VI)'
        # should return  0 since there's no way to sort definitively
        assert refindex.prepare_book_page_sort(reference) == 0
