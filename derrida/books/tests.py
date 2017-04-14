from collections import defaultdict
import csv
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.utils.safestring import mark_safe
from django.test import TestCase
try:
    # django 1.10
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
import json
from unittest.mock import patch
import os
from io import StringIO

# All the models
from .models import *

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    'fixtures')

class TestOwningInstitution(TestCase):
    fixtures = ['sample_book_data.json']

    def test_str(self):
        long_name = 'New York Society Library'
        short_name = 'NYSL'
        inst = OwningInstitution(name=long_name)
        # should use long name if no short name is set
        assert str(inst) == long_name
        inst.short_name = short_name
        assert str(inst) == short_name

    def test_book_count(self):
        # test abstract book count mix-in via owning institution model
        # tests that html for admin form is rendered correctly

        pl = Place.objects.first()
        inst = OwningInstitution.objects.create(name='NYSL',
            place=pl)
        # new institution has no books associated
        base_url = reverse('admin:books_book_changelist')
        assert inst.book_count() == \
            mark_safe('<a href="%s?%ss__id__exact=%s">%s</a>' %
                (base_url,
                inst.__class__.__name__.lower(),
                inst.pk,
                0)
            )

        # create a book and associated it with the institution
        book = ItemType.objects.get(name='Book')
        pub = Publisher.objects.create(name='Pub Lee')
        bk = Book.objects.create(primary_title='Some rambling long old title',
            short_title='Some rambling',
            item_type=book,
            original_pub_info='foo',
            publisher=pub, pub_place=pl, work_year=1823,
            is_extant=False, is_annotated=False, is_digitized=False)

        cat = Catalogue.objects.create(institution=inst, book=bk,
            is_current=False)


        assert inst.book_count() == \
            mark_safe('<a href="%s?%ss__id__exact=%s">%s</a>' %
                (base_url,
                inst.__class__.__name__.lower(),
                inst.pk,
                1)
            )


class TestBook(TestCase):
    fixtures = ['sample_book_data.json']

    def test_str(self):
        la_vie = Book.objects.get(short_title__contains="La vie")

        assert '%s (%s)' % (la_vie.short_title, la_vie.copyright_year) \
            == str(la_vie)

    def test_catalogue_call_numbers(self):
        la_vie = Book.objects.get(short_title__contains="La vie")

        # fixture has no call number (shelf-mark) with
        assert la_vie.catalogue_call_numbers() == ''

        # add a first and second catalogue record
        owning_inst = OwningInstitution.objects.first()
        cat = Catalogue.objects.create(institution=owning_inst,
            book=la_vie, call_number='NY789', is_current=True)
        assert la_vie.catalogue_call_numbers() == 'NY789'
        cat = Catalogue.objects.create(institution=owning_inst,
            book=la_vie, call_number='PU456', is_current=True)
        assert la_vie.catalogue_call_numbers() == 'NY789, PU456'

    def test_authors(self):
        la_vie = Book.objects.get(short_title__contains="La vie")

        levi = 'L\u00e9vi-Strauss'
        assert la_vie.authors().count() == 1
        assert la_vie.authors().first().person.authorized_name == \
            levi
        assert la_vie.author_names() == levi

        # modify fixture data to test two authors
        jacques = 'Derrida, Jacques'
        derrida = Person.objects.get(authorized_name=jacques)
        creator_author = CreatorType.objects.get(name='Author')
        Creator.objects.create(creator_type=creator_author,
            person=derrida, book=la_vie)
        assert la_vie.authors().count() == 2
        assert la_vie.author_names() == '%s, %s' % (levi, jacques)

        # and no authors
        la_vie.creator_set.all().delete()
        assert la_vie.authors().count() == 0

    def test_add_author(self):
        la_vie = Book.objects.get(short_title__contains="La vie")
        derrida = Person.objects.get(authorized_name="Derrida, Jacques")
        la_vie.add_author(derrida)
        # check that appropriate creator model was created
        assert Creator.objects.filter(creator_type__name='Author',
            person=derrida, book=la_vie).count() == 1
        assert la_vie.authors().count() == 2

    def test_add_editor(self):
        la_vie = Book.objects.get(short_title__contains="La vie")
        derrida = Person.objects.get(authorized_name="Derrida, Jacques")
        la_vie.add_editor(derrida)
        # check that appropriate creator model was created
        assert Creator.objects.filter(creator_type__name='Editor',
            person=derrida, book=la_vie).count() == 1

    def test_add_translator(self):
        la_vie = Book.objects.get(short_title__contains="La vie")
        derrida = Person.objects.get(authorized_name="Derrida, Jacques")
        la_vie.add_translator(derrida)
        # check that appropriate creator model was created
        assert Creator.objects.filter(creator_type__name='Translator',
            person=derrida, book=la_vie).count() == 1


class TestCatalogue(TestCase):

    def test_str(self):
        # create a book and owning institution to link

        pub = Publisher(name='Pub Lee')
        pub_place = Place(name='Printington', geonames_id=4567)
        inst = OwningInstitution(name='NYSL')
        bk = Book(primary_title='Some rambling long old title',
            short_title='Some rambling',
            original_pub_info='foo',
            publisher=pub,
            pub_place=pub_place,
            work_year=1823)

        cat = Catalogue(institution=inst, book=bk)
        assert '%s / %s' % (bk, inst) == str(cat)

        # with no date set
        cat.start_year = 1891
        assert '%s / %s (1891-)' % (bk, inst) == str(cat)
