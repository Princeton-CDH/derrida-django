# -*- coding: utf-8 -*-
from collections import defaultdict
import os
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from pandas import DataFrame

# All the models
from derrida.places.models import Place
# Common models between projects and associated new types
from derrida.books.models import AssociatedBook, Book, Catalogue, Creator, CreatorType, \
    ItemType, Publisher, OwningInstitution
# Citationality extensions
from derrida.books.models import DerridaWork, DerridaWorkBook, Reference, ReferenceType, \
    Work
from derrida.books.management.commands import import_zotero


FIXTURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '..', 'fixtures')


class TestImportZotero(TestCase):

    test_csv = os.path.join(FIXTURE_DIR, 'test_zotero_data.csv')

    def setUp(self):

        self.cmd = import_zotero.Command()
        self.cmd.stdout = StringIO()
        self.cmd.stats = defaultdict(int)
        self.cmd.dud_code_list = []

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
            'Abstract Note',
            'Notes',
            'Manual Tags',
            'Pages',
            'Publication Title',
            ]

        for column in wanted_columns:
            assert column in data

    def test_parse_ref_tag(self):
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
        dg = DerridaWork.objects.get(short_title='De la grammatologie')
        # Get a tag that's a full format
        full_tag = 'dg109cF10sU'

        self.cmd.parse_ref_tag(full_tag, bk)
        reference = Reference.objects.get(book=bk)
        assert reference.derridawork == dg
        assert reference.derridawork_page == '109'
        assert reference.derridawork_pageloc == 'c'
        assert reference.reference_type.name == 'Footnote'
        # page + sequelae
        assert reference.book_page == '10s'
        # Unknown if it's annotated or not, s
        self.assertFalse(bk.is_extant)
        self.assertFalse(bk.is_annotated)
        # Make sure two can be added by the short_description
        full_tag = 'dg111cF10sU'
        self.cmd.parse_ref_tag(full_tag, bk)
        references = Reference.objects.filter(book=bk)
        assert len(references) == 2
        for reference in references:
            reference.delete()

        # Now play with tag types
        full_tag = 'dg112eF(IV)sU'
        self.cmd.parse_ref_tag(full_tag, bk)
        reference = Reference.objects.get(book=bk)
        assert reference.book_page == '(IV)s'
        reference.delete()

        full_tag = 'dg112eQ(IV)sU'
        self.cmd.parse_ref_tag(full_tag, bk)
        reference = Reference.objects.get(book=bk)
        assert reference.reference_type.name == 'Quotation'
        reference.delete()

        # provisional tag has no book page
        full_tag = 'dg112eQ___'
        self.cmd.parse_ref_tag(full_tag, bk)
        reference = Reference.objects.get(book=bk)
        assert reference.reference_type.name == 'Quotation'
        assert reference.book_page == ''
        reference.delete()

    def test_create_book(self):
        data = self.cmd.clean_data(self.test_csv)
        rows = []
        for index, row in data.iterrows():
            rows.append(row)
        de_gram = rows[0]

        # Make the first work - journal article
        article = ItemType.objects.get(name='Journal Article')
        self.cmd.create_book(de_gram)
        book = Book.objects.get(short_title__contains='De la')
        assert book.primary_title == de_gram['Title']
        assert book.short_title == ' '.join(de_gram['Title'].split()[0:4])
        # No publisher so should be None
        self.assertFalse(book.original_pub_info)
        assert book.page_range ==  de_gram['Pages']
        # Reflecting no finding aid and annotations need to be set
        # manually, defaulting to false
        self.assertFalse(book.is_annotated)
        self.assertFalse(book.is_extant)
        assert book.item_type == article
        assert book.copyright_year == 1965
        # Make sure the author was associated
        assert book.authors().count() == 1
        derrida = 'Derrida, Jacques'
        assert book.authors().first().person.authorized_name == derrida
        # Make sure a catalogue exists for Princeton
        catalogue = Catalogue.objects.get(book=book)
        assert catalogue.institution.short_name == 'PUL'
        # There should be one tag
        references = Reference.objects.filter(book=book)
        assert references.count() == 1
        # Check a book with notes fields of some sorts
        idees = rows[4]
        self.cmd.create_book(idees)
        book = Book.objects.get(short_title__contains='Idées')
        assert book.notes
        # Only one of three note fields set
        assert book.notes == idees['Abstract Note']
        # Let's fix that
        book.delete()
        idees['Notes'] = 'Notes field'
        idees['Extra'] = 'Extra field'
        self.cmd.create_book(idees)
        book = Book.objects.get(short_title__contains='Idées')
        # Now all three should exist on their own separate line
        assert book.notes == '\n'.join([idees['Notes'],
                                      idees['Extra'],
                                      idees['Abstract Note']])

        # Faked New York to check place setting functioning correctly
        assert book.pub_place == Place.objects.get(name='New York')

