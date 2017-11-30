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

    def test_prepare_instance_slug(self):

        # create a ReferenceIndex object
        refindex = ReferenceIndex()
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
