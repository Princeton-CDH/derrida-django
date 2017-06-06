# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
import pytest

# All the models
from derrida.places.models import Place
from derrida.people.models import Person
# Common models between projects and associated new types
from derrida.books.models import AssociatedBook, Book, Catalogue, Creator, \
    CreatorType, ItemType, Publisher, OwningInstitution, Journal
# Citationality extensions
from derrida.books.models import DerridaWork, DerridaWorkBook, Reference, \
    ReferenceType, Work, Instance, InstanceCatalogue, WorkLanguage, \
    InstanceLanguage, Language, WorkSubject, Subject


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

    def test_instance_count(self):
        # test abstract book count mix-in via owning institution model
        # tests that html for admin form is rendered correctly

        pl = Place.objects.first()
        inst = OwningInstitution.objects.create(name='NYSL',
            place=pl)
        # new institution has no books associated
        change_url = reverse('admin:books_instance_changelist')
        admin_book_count = inst.instance_count()
        assert change_url in admin_book_count
        assert 'id__exact=%s' % inst.pk in admin_book_count
        assert '0' in admin_book_count

        # create a book and associated it with the institution
        book = ItemType.objects.get(name='Book')
        pub = Publisher.objects.create(name='Pub Lee')
        wk = Work.objects.create(primary_title='Some title')
        instance = Instance.objects.create(work=wk)
         # publisher=pub, pub_place=pl,
            # is_extant=False, is_annotated=False, is_digitized=False)

        cat = InstanceCatalogue.objects.create(institution=inst,
            instance=instance, is_current=False)

        inst_book_count = inst.instance_count()
        assert change_url in inst_book_count
        assert 'id__exact=%s' % inst.pk in inst_book_count
        assert '1' in inst_book_count


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

            # Check the reverse association
            assoc, c = AssociatedBook.objects.get(
                from_book=bk,
                to_book=la_vie,
            )
            assert assoc.is_collection



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

class TestReference(TestCase):

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

    def test_str(self):
        bk1 = Book.objects.get(short_title='Some rambling')
        dg = DerridaWork.objects.get(pk=1)
        quotation = ReferenceType.objects.get(name='Quotation')
        # Writing this out because complicated output
        desired_output = 'De la grammatologie, 110a: Some rambling, 10s, Quotation'
        reference, created = Reference.objects.get_or_create(
            book=bk1,
            derridawork=dg,
            derridawork_page='110',
            derridawork_pageloc='a',
            book_page='10s',
            reference_type=quotation
        )
        assert str(reference) == desired_output

    def test_associate_with_book_and_derrida_work(self):
        bk1 = Book.objects.get(short_title='Some rambling')
        dg = DerridaWork.objects.get(pk=1)
        quotation = ReferenceType.objects.get(name='Quotation')
        # Writing this out because complicated output
        desired_output = 'De la grammatologie, 110a: Some rambling, 10s, Quotation'
        reference, created = Reference.objects.get_or_create(
            book=bk1,
            derridawork=dg,
            derridawork_page='110',
            derridawork_pageloc='a',
            book_page='10s',
            reference_type=quotation
        )
        reference2, created = Reference.objects.get_or_create(
            book=bk1,
            derridawork=dg,
            derridawork_page='113',
            derridawork_pageloc='b',
            book_page='10s',
            reference_type=quotation
        )
        # Make sure that more than one reference can be linked
        references = Reference.objects.filter(book=bk1)
        assert references.count() == 2
        for ref in references:
            assert ref.book == bk1
            assert ref.derridawork == dg

        # Delete one and check counts
        references[0].delete()
        references = Reference.objects.filter(book=bk1)
        assert references.count() == 1


class TestWork(TestCase):
    fixtures = ['sample_work_data.json']

    def test_str(self):
        la_vie = Work.objects.get(short_title__contains="La vie")
        assert '%s (%s)' % (la_vie.short_title, la_vie.year) \
            == str(la_vie)
        # no date
        la_vie.year = None
        assert '%s (n.d.)' % (la_vie.short_title, )

    def test_author_names(self):
        la_vie = Work.objects.get(short_title__contains="La vie")
        assert la_vie.author_names() == "L\u00e9vi-Strauss"

    def test_instance_count(self):
        la_vie = Work.objects.get(short_title__contains="La vie")
        inst_count = la_vie.instance_count()
        instance_list_url = reverse('admin:books_instance_changelist')
        assert instance_list_url in inst_count
        assert 'id__exact=%s' % la_vie.pk in inst_count
        assert '1' in inst_count


class TestInstance(TestCase):
    fixtures = ['sample_work_data.json']

    def test_display_title(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        # short title from work if no alternate title
        assert la_vie.display_title() == la_vie.work.short_title
        # alternate title from instance if set
        la_vie.alternate_title = 'Family Life'
        assert la_vie.display_title() == la_vie.alternate_title

    def test_str(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        assert '%s (%s)' % (la_vie.display_title(), la_vie.copyright_year) \
            == str(la_vie)
        # no date
        la_vie.year = None
        assert '%s (n.d.)' % (la_vie.display_title(), )

    def test_item_type(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        assert la_vie.item_type == 'Book'

        # journal article
        la_vie.journal = Journal.objects.all().first()
        assert la_vie.item_type == 'Journal Article'

        # book section
        la_vie.journal = None
        la_vie.collected_in = Instance()
        assert la_vie.item_type == 'Book Section'

    def test_author_names(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        assert la_vie.author_names() == la_vie.work.author_names()

    def test_catalogue_call_number(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        # fixture has no call number (shelf-mark)
        assert la_vie.catalogue_call_numbers() == ''

        # add a first and second catalogue record
        owning_inst = OwningInstitution.objects.first()
        InstanceCatalogue.objects.create(institution=owning_inst,
            instance=la_vie, call_number='NY789', is_current=True)
        assert la_vie.catalogue_call_numbers() == 'NY789'
        InstanceCatalogue.objects.create(institution=owning_inst,
            instance=la_vie, call_number='PU456', is_current=True)
        assert la_vie.catalogue_call_numbers() == 'NY789, PU456'

    def test_clean(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        la_vie.journal = Journal.objects.all().first()
        la_vie.collected_in = Instance()
        with pytest.raises(ValidationError) as err:
            la_vie.clean()
        assert 'Cannot belong to both a journal and a collection' in str(err)


class TestWorkLanguage(TestCase):
    fixtures = ['sample_work_data.json']

    def test_str(self):
        la_vie = Work.objects.get(short_title__contains="La vie")
        fr = Language.objects.get(name='French')
        wklang = WorkLanguage(language=fr, work=la_vie)
        assert str(wklang) == '%s %s' % (la_vie, fr)

        wklang.is_primary = True
        assert str(wklang) == '%s %s (primary)' % (la_vie, fr)


class TestWorkSubject(TestCase):
    fixtures = ['sample_work_data.json']

    def test_str(self):
        la_vie = Work.objects.get(short_title__contains="La vie")
        ling = Subject(name='Linguistics')
        wksubj = WorkSubject(work=la_vie, subject=ling)
        assert str(wksubj) == '%s %s' % (la_vie, ling)

        wksubj.is_primary = True
        assert str(wksubj) == '%s %s (primary)' % (la_vie, ling)

    def test_work_count(self):
        # test abstract work count mix-in via owning subject model
        # tests that html for admin form is rendered correctly
        la_vie = Work.objects.get(short_title__contains="La vie")
        subj = Subject.objects.create(name='Linguistics')
        # new subject has no books associated
        change_url = reverse('admin:books_work_changelist')
        admin_work_count = subj.work_count()
        assert change_url in admin_work_count
        assert 'id__exact=%s' % la_vie.pk in admin_work_count
        assert '0' in admin_work_count

        # add a work/subject
        WorkSubject.objects.create(work=la_vie, subject=subj)
        admin_work_count = subj.work_count()
        assert '1' in admin_work_count


class TestInstanceLanguage(TestCase):
    fixtures = ['sample_work_data.json']

    def test_str(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        ger = Language.objects.get(name='German')
        instlang = InstanceLanguage(language=ger, instance=la_vie)
        assert str(instlang) == '%s %s' % (la_vie, ger)

        instlang.is_primary = True
        assert str(instlang) == '%s %s (primary)' % (la_vie, ger)


class TestInstanceCatalogue(TestCase):
    fixtures = ['sample_work_data.json']

    def test_str(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")

        inst_cat = la_vie.instancecatalogue_set.first()
        assert str(inst_cat) == '%s / %s' % (la_vie, inst_cat.institution)

        # with dates
        inst_cat.start_year = 1891
        assert str(inst_cat) == '%s / %s (1891-)' % (la_vie, inst_cat.institution)




