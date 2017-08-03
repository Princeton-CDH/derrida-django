# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from djiffy.models import Manifest
import pytest
import json

from derrida.places.models import Place
from derrida.people.models import Person
# Common models between projects and associated new types
from derrida.books.models import CreatorType, Publisher, OwningInstitution, \
    Journal, DerridaWork, Reference, \
    ReferenceType, Work, Instance, InstanceCatalogue, WorkLanguage, \
    InstanceLanguage, Language, WorkSubject, Subject
from derrida.interventions.models import Canvas

class TestOwningInstitution(TestCase):
    fixtures = ['sample_work_data.json']

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
        short_title = 'Ceci n\'est pas un livre'
        testwork = DerridaWork.objects.get(short_title=short_title)
        assert str(testwork) == short_title


class TestReference(TestCase):
    fixtures = ['sample_work_data.json']

    def setUp(self):
        self.manif = Manifest.objects.create()
        self.la_vie = Instance.objects.get(work__short_title__contains="La vie")
        self.dg = DerridaWork.objects.get(pk=1)
        self.quotation = ReferenceType.objects.get(name='Quotation')

    def test_str(self):
        # Writing this out because complicated output
        desired_output = 'De la grammatologie, 110a: %s, 10s, Quotation' % \
            self.la_vie.display_title()
        reference = Reference.objects.create(
            instance=self.la_vie,
            derridawork=self.dg,
            derridawork_page='110',
            derridawork_pageloc='a',
            book_page='10s',
            reference_type=self.quotation
        )
        assert str(reference) == desired_output

    def test_valid_autocompletes(self):
        la_vie = self.la_vie
        reference = Reference.objects.create(
            instance=la_vie,
            derridawork=self.dg,
            derridawork_page='110',
            derridawork_pageloc='a',
            book_page='10s',
            reference_type=self.quotation
        )

        # no instances have associated canvases so this should return an
        # empty list as a JSON string
        data = reference.get_autocomplete_instances()
        assert json.loads(data) == []

        # add a canvas to la_vie, then it should appear in the list
        la_vie.digital_edition = self.manif
        la_vie.save()
        data = reference.get_autocomplete_instances()
        assert json.loads(data) == [la_vie.pk]

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

    def test_is_digitized(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        assert not la_vie.is_digitized()

        la_vie.digital_edition = Manifest()
        assert la_vie.is_digitized()

    def test_location(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        # grabs first two dashed segments
        la_vie.digital_edition = Manifest(
            label='Shelf - By the Cupboard - Title'
        )
        assert la_vie.location == 'Shelf - By the Cupboard'
        # test the one variation in the pattern
        la_vie.digital_edition = Manifest(
            label='House - Gift and ... Items - Title'
        )
        assert la_vie.location == 'House'



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
