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
import re
from io import StringIO

# Import commmand
from .management.commands import import_zotero

# All the models
from derrida.places.models import Place
from derrida.people.models import Person
from .models import AssociatedBook, Book, Catalogue, Creator, CreatorType, \
    ItemType, Publisher, OwningInstitution
from .models import DerridaWork, DerridaWorkBook

# pandas
from pandas import DataFrame


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

    def test_get_parent(self):
        # Book shouldn't have a parent
        la_vie = Book.objects.get(short_title__contains="La vie")
        self.assertFalse(la_vie.get_parent())

        pub, created = Publisher.objects.get_or_create(name='Pub Lee')
        pub_place, created = Place.objects.get_or_create(
            name='Printington',
            geonames_id=4567,
            latitude=0,
            longitude=0
        )
        section = ItemType.objects.get(name='Book Section')
        bk, created = Book.objects.get_or_create(
            primary_title='Some rambling long old title',
            item_type=section,
            short_title='Some rambling',
            original_pub_info='foo',
            publisher=pub,
            pub_place=pub_place,
            work_year=1823
        )

        self.assertFalse(bk.get_parent())

        assoc, c = AssociatedBook.objects.get_or_create(
            from_book=la_vie,
            to_book=bk,
            is_collection=True
        )
        assert c
        assert assoc.is_collection
        assert bk.get_parent() == la_vie
        # Make sure the book/section distinction holds
        self.assertFalse(la_vie.get_parent())

        def test_get_children(self):
            # Book shouldn't have any children
            la_vie = Book.objects.get(short_title__contains="La vie")
            self.assertFalse(la_vie.get_children())

            pub, created = Publisher.objects.get_or_create(name='Pub Lee')
            pub_place, created = Place.objects.get_or_create(
                name='Printington',
                geonames_id=4567,
                latitude=0,
                longitude=0
            )
            section = ItemType.objects.get(name='Book Section')
            bk, created = Book.objects.get_or_create(
                primary_title='Some rambling long old title',
                item_type=section,
                short_title='Some rambling',
                original_pub_info='foo',
                publisher=pub,
                pub_place=pub_place,
                work_year=1823
            )

            self.assertFalse(bk.get_parent())

            assoc, c = AssociatedBook.objects.get_or_create(
                from_book=la_vie,
                to_book=bk,
                is_collection=True
            )
            assert c
            assert assoc.is_collection
            assert la_vie.get_children().first() == bk
            assert len(la_vie.get_children()) == 1
            # Make a new book
            bk, created = Book.objects.get_or_create(
                primary_title='Some rambling long old title 2',
                item_type=section,
                short_title='Some rambling 2',
                original_pub_info='foo',
                publisher=pub,
                pub_place=pub_place,
                work_year=1823
            )

            # We haven't associated it yet
            assert len(la_vie.get_children()) == 1

            assoc, c = AssociatedBook.objects.get_or_create(
                from_book=la_vie,
                to_book=bk,
                is_collection=True
            )
            # Now we have
            assert c
            assert assoc.is_collection
            assert la_vie.get_children().first() == bk
            assert len(la_vie.get_children()) == 2


class TestAssociatedBook(TestCase):

    def setUp(self):
        section = ItemType.objects.get(name='Book Section')
        pub, created = Publisher.objects.get_or_create(name='Pub Lee')
        pub_place, created = Place.objects.get_or_create(
            name='Printington',
            geonames_id=4567,
            latitude=0,
            longitude=0
        )

        bk1, created = Book.objects.get_or_create(
            primary_title='Some rambling long old title',
            item_type=section,
            short_title='Some rambling',
            original_pub_info='foo',
            publisher=pub,
            pub_place=pub_place,
            work_year=1823
        )
        bk2, created = Book.objects.get_or_create(
            primary_title='Some rambling long old title: the sequel',
            item_type=section,
            short_title='Some rambling 2',
            original_pub_info='foo',
            publisher=pub,
            pub_place=pub_place,
            work_year=1823
        )

    def test_str(self):
        books = Book.objects.all()
        association = AssociatedBook(
            from_book=books[0],
            to_book=books[1],
        )

        assert str(association) == 'Some rambling - Some rambling 2'

    def test_signals(self):
        '''Checks the signals in signals.py for books module.
        Should produce reciprocal creation and deletion'''
        books = Book.objects.all()
        association, created = AssociatedBook.objects.get_or_create(
            from_book=books[0],
            to_book=books[1],
        )

        assert created

        # Refresh the object
        books = Book.objects.all()

        # Test the link
        assoc_books = books[0].books.all()
        print(assoc_books)
        assert len(assoc_books) == 1
        assert assoc_books[0] == books[1]

        # Reverse it
        assoc_books = books[1].books.all()
        assert len(assoc_books) == 1
        assert assoc_books[0] == books[0]

        # Delete it
        association.delete()

        # Check again
        assoc_books = books[0].books.all()
        assert len(assoc_books) == 0

        # Reverse it
        assoc_books = books[1].books.all()
        assert len(assoc_books) == 0


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


class TestDerridaWork(TestCase):

    def setUp(self):
        testwork, c = DerridaWork.objects.get_or_create(
            short_title='Ceci n\'est pas un livre',
            full_citation=('Ceci n\'est pas un livre: '
                           'and other tales of deconstructionism'),
            is_primary=True,
        )


    def test_str(self):
        '''Test that DerridaWork produces its expected string'''
        short_title='Ceci n\'est pas un livre'
        testwork = DerridaWork.objects.get(short_title=short_title)
        assert str(testwork) == short_title


class TestDerridaWorkBook(TestCase):

    def setUp(self):
        testwork, c = DerridaWork.objects.get_or_create(
            short_title='Ceci n\'est pas un livre',
            full_citation=('Ceci n\'est pas un livre: '
                           'and other tales of deconstructionism'),
            is_primary=True,
        )


    def test_associate_with_cited_book(self):
        '''Tests that DerridaWork and Book can be associated
        as the edition cited in the platonic DerridaWork'''
        pub, created = Publisher.objects.get_or_create(name='Pub Lee')
        pub_place, created = Place.objects.get_or_create(
            name='Printington',
            geonames_id=4567,
            latitude=0,
            longitude=0
        )
        book = ItemType.objects.get(name='Book')
        bk, created = Book.objects.get_or_create(
            primary_title='Some rambling long old title',
            item_type=book,
            short_title='Some rambling',
            original_pub_info='foo',
            publisher=pub,
            pub_place=pub_place,
            work_year=1823
        )
        short_title='Ceci n\'est pas un livre'
        testwork = DerridaWork.objects.get(short_title=short_title)

        new_assoc, created = DerridaWorkBook.objects.get_or_create(
            derridawork=testwork,
            book=bk,
        )

        assert created
        assert new_assoc.derridawork == testwork
        assert new_assoc.book == bk
        assert (testwork.cited_books).first() == bk


class TestImportZotero(TestCase):

    test_csv = os.path.join(FIXTURE_DIR, 'test_zotero_data.csv')

    def setUp(self):

        self.cmd = import_zotero.Command()
        self.cmd.stdout = StringIO()
        self.cmd.stats = defaultdict(int)

        # Kludge to get dummy values in the command we're using to test for
        # API lookups, since we're already hacking it a bit.
        # TODO: Figure out how to mock this instead
        def dummy_viaf(*args, **kwargs):
            return 'http://totallyviaf.org/viaf/00001/'
        def dummy_geonames(*args, **kwargs):
            return {
                'latitude': 0,
                'longitude': 0,
                'geonames_id': 'http://notgeonames/0001/'
            }

        self.cmd.viaf_lookup = dummy_viaf
        self.cmd.geonames_lookup = dummy_geonames

        princeton, created = Place.objects.get_or_create(
            name='Princeton, NJ',
            **(self.cmd.geonames_lookup('Princeton, NJ'))
        )
        OwningInstitution.objects.get_or_create(
            short_name='PUL',
            contact_info='http://library.princeton.edu/help/contact-us',
            place=princeton
        )

    def test_run(self):
            out = StringIO()
            # pass the modified self.cmd object
            call_command(self.cmd, self.test_csv, stdout=out)
            output = out.getvalue()
            assert '5 books' in output
            assert '2 places' in output
            assert '7 people' in output
            assert '2 publishers' in output
            assert '23 references from tags' in output

            assert '0 errors' in output
            assert 'following tags looked suspicious' not in output
            assert '0 references with unset tags'

    def test_clean_data(self):
        data = self.cmd.clean_data(self.test_csv)
        assert isinstance(data, DataFrame)
        wanted_columns = [
            'Key',
            'Item Type',
            'Date',
            'Author',
            'Title',
            'Translator',
            'Editor',
            'Series Editor',
            'Url',
            'Publisher',
            'Place',
            'Language',
            'Extra',
            'Notes',
            'Manual Tags',
            'Pages',
            'Publication Title',
            ]

        for column in wanted_columns:
            assert column in data

    def test_create_book(self):
        data = self.cmd.clean_data(self.test_csv)
        rows = []
        for index, row in data.iterrows():
            rows.append(row)
        de_gram = rows[0]

        # Make the first work - journal article
        self.cmd.create_book(de_gram)
        book = Book.objects.get(short_title__contains='De la')
        assert book.primary_title == de_gram['Title']
        self.assertFalse(book.is_extant)

        # Make sure the author was associated
        assert book.authors().count() == 1
        derrida = 'Derrida, Jacques'
        assert book.authors().first().person.authorized_name == derrida
