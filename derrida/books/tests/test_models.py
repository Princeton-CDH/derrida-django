# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse, resolve
from djiffy.models import Manifest, Canvas
import pytest
import json

from derrida.places.models import Place
from derrida.books.models import Publisher, OwningInstitution, \
    Journal, DerridaWork, DerridaWorkSection, Reference, \
    ReferenceType, Work, Instance, InstanceCatalogue, WorkLanguage, \
    InstanceLanguage, Language, WorkSubject, Subject
from derrida.interventions.models import Intervention
from derrida.people.models import Person


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


class TestDerridaSection(TestCase):

    def test_str(self):
        assert str(DerridaWorkSection(name='Chapter 1')) == 'Chapter 1'


class TestReference(TestCase):
    fixtures = ['sample_work_data']

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

    def test_get_absolute_url(self):
        ref = Reference.objects.create(
            instance=self.la_vie,
            derridawork=self.dg,
            derridawork_page='110',
            derridawork_pageloc='a',
            book_page='10s',
            reference_type=self.quotation
        )
        ref_url = ref.get_absolute_url()
        resolved_url = resolve(ref_url)
        assert resolved_url.url_name == 'reference'
        assert resolved_url.namespace == 'books'
        assert resolved_url.kwargs['derridawork_slug'] == self.dg.slug
        assert resolved_url.kwargs['page'] == ref.derridawork_page
        assert resolved_url.kwargs['pageloc'] == ref.derridawork_pageloc

    def test_instance_ids_with_digital_editions(self):
        # check static method, so we don't need cls or self
        Reference.instance_ids_with_digital_editions()

        # no instances have associated canvases so this should return an
        # empty list as a JSON string
        data = Reference.instance_ids_with_digital_editions()
        assert json.loads(data) == []

        # add a canvas to la_vie, then it should appear in the list
        self.la_vie.digital_edition = self.manif
        self.la_vie.save()
        data = Reference.instance_ids_with_digital_editions()
        assert json.loads(data) == [self.la_vie.pk]

    def test_instance_slug(self):
        # create a reference
        ref = Reference.objects.create(
            instance=self.la_vie,
            derridawork=self.dg,
            derridawork_page='110',
            derridawork_pageloc='a',
            book_page='10s',
            reference_type=self.quotation
        )
        # not a book section (none in test set are)
        # should return the slug of its instance
        assert ref.instance_slug == self.la_vie.slug

        # make work into a book section as a 'collected in'
        la_vie_collected = Instance.objects.create(work=self.la_vie.work,
            slug='la-vie-collected')
        self.la_vie.collected_in = la_vie_collected
        self.la_vie.save()
        # should return the slug for the collection
        assert ref.instance_slug == la_vie_collected.slug

    def test_get_instance_url(self):
        # create a reference
        ref = Reference.objects.create(
            instance=self.la_vie,
            derridawork=self.dg,
            derridawork_page='110',
            derridawork_pageloc='a',
            book_page='10s',
            reference_type=self.quotation
        )
        # not a book section (none in test set are)
        # should return the slug of its instance
        assert ref.instance_url == self.la_vie.get_absolute_url()

        # make work into a book section as a 'collected in'
        la_vie_collected = Instance.objects.create(work=self.la_vie.work,
            slug='la-vie-collected')
        self.la_vie.collected_in = la_vie_collected
        self.la_vie.save()
        # should return the slug for the collection
        assert ref.instance_url == la_vie_collected.get_absolute_url()


class TestReferenceQuerySet(TestCase):
    fixtures = ['test_references.json']

    def setUp(self):
        self.ref_qs = Reference.objects.all()

    def test_order_by_source_page(self):
        pages = sorted([ref.derridawork_page for ref in self.ref_qs.all()])
        assert list(Reference.objects.order_by_source_page()
                             .values_list('derridawork_page', flat=True)) \
                == pages

    def test_order_by_author(self):
        authors = sorted(
            ['; '.join([str(p) for p in ref.instance.work.authors.all()])
             for ref in self.ref_qs])
        qs_authors = list(self.ref_qs.order_by_author() \
           .values_list('instance__work__authors__authorized_name', flat=True))
        qs_authors = ['' if name is None else name for name in qs_authors]
        assert qs_authors == authors

    def test_summary_values(self):
        ref = self.ref_qs.first()
        ref_values = self.ref_qs.summary_values().first()
        assert ref_values['id'] == ref.pk
        assert ref_values['instance__slug'] == ref.instance.slug
        assert ref_values['derridawork__slug'] == ref.derridawork.slug
        assert ref_values['derridawork_page'] == ref.derridawork_page
        assert ref_values['derridawork_pageloc'] == ref.derridawork_pageloc
        assert ref_values['author'] == \
            ref.instance.work.authors.first().authorized_name

        # TODO: not actually sure how this works for multi-author items


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
        la_vie.copyright_year = None
        assert '%s (n.d.)' % (la_vie.display_title(), )

    def test_generate_base_slug(self):
        work = Work.objects.create(primary_title='Ulysses')
        inst = Instance(work=work)
        # short title, no author or year
        assert inst.generate_base_slug() == 'ulysses'

        # single-name author
        joyce = Person.objects.create(authorized_name='Joyce')
        work.authors.add(joyce)
        assert inst.generate_base_slug() == 'joyce-ulysses'
        # comma-delimited author name
        joyce.authorized_name = 'Joyce, James'
        joyce.save()
        assert inst.generate_base_slug() == 'joyce-ulysses'

        # work year - used if no instance copyright year
        work.year = 1922
        work.save()
        assert inst.generate_base_slug() == 'joyce-ulysses-1922'
        # copyright year used when available
        inst.copyright_year = 1950
        assert inst.generate_base_slug() == 'joyce-ulysses-1950'

        # long titles truncated to ten words
        work.primary_title = 'A portrait of the artist as a young man: ' + \
            ' the strange story of Stephen Dedalus'
        work.save()
        assert inst.generate_base_slug() == 'joyce-a-portrait-of-the-artist-as-a-young-man-1950'

    def test_generate_safe_slug(self):

        # la vie should appear in the list and see itself so suggest -B
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        assert la_vie.generate_safe_slug() == la_vie.generate_base_slug() + '-B'
        # save the -B copy
        la_vie.pk = None
        la_vie.slug = la_vie.generate_safe_slug()
        la_vie.save()
        # now pull in the original copy and run again, should produce a slug
        # with -C as its suffix
        la_vie = Instance.objects.get(slug=la_vie.generate_base_slug())
        la_vie.generate_safe_slug() == la_vie.generate_base_slug() + '-C'
        # get the original again, and see if a duplicate will produce the -C ending
        la_vie = Instance.objects.filter(work__short_title__contains="La vie").order_by('slug')[0]
        la_vie.pk = None
        la_vie.slug = ''
        la_vie.save()
        la_vie.refresh_from_db()
        assert la_vie.slug == la_vie.generate_base_slug() + '-C'

    def test_save(self):
        # on save, if empty slug, should set one with generate safe slug
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        la_vie.slug = ''
        expected_slug = la_vie.generate_safe_slug()
        la_vie.save()
        la_vie.refresh_from_db()
        assert la_vie.slug == expected_slug

    def test_get_absolute_url(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        item_url = la_vie.get_absolute_url()
        resolved_url = resolve(item_url)
        assert resolved_url.url_name == 'detail'
        assert resolved_url.namespace == 'books'
        assert resolved_url.kwargs['slug'] == la_vie.slug

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
        # location is based on first part of manifest title
        la_vie.digital_edition = Manifest(
            label='Shelf - By the Cupboard - Title'
        )
        assert la_vie.location == 'Shelf, By the Cupboard'

        # some manifests have only one location, and second part
        # indicates it is a gift
        la_vie.digital_edition = Manifest(
            label='House - Gift Books, Works By and About Derrida, and Related Items - Derrida, Jacques. De la grammatologie.'
        )
        assert la_vie.location == 'House'

    def test_year(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        # print year not known - use copyright year
        assert la_vie.year == la_vie.copyright_year
        # use print year if known
        la_vie.print_date = datetime(year=1965, month=1, day=1)
        assert la_vie.year == la_vie.print_date.year
        # nothing known
        la_vie.print_date_year_known = False
        la_vie.copyright_year = None
        assert la_vie.year is None

    def test_images(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        # no digital edition - empty queryset
        assert la_vie.images().count() == 0
        # digital edition, no pages
        la_vie.digital_edition = mfst = Manifest.objects.create(short_id='m1')
        assert la_vie.images().count() == 0
        Canvas.objects.bulk_create([
            Canvas(manifest=mfst, label='p1', order=1, short_id='c1'),
            Canvas(manifest=mfst, label='p2', order=2, short_id='c2'),
            Canvas(manifest=mfst, label='p3', order=3, short_id='c3'),
        ])
        assert la_vie.images().count() == 3
        assert Canvas.objects.first() in la_vie.images()

    def test_overview_images(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        # no digital edition - empty queryset
        assert la_vie.overview_images().count() == 0
        # digital edition, no pages
        la_vie.digital_edition = mfst = Manifest.objects.create(short_id='m1')
        assert la_vie.overview_images().count() == 0
        # create some test canvases to include/exclude
        outside_views = ['Front Cover', 'Inside Cover', 'Back Cover',
            'Spine', 'Edge View']
        for i, label in enumerate(outside_views):
            Canvas.objects.create(manifest=mfst, label=label,
                short_id='cover%d' % i, order=i)
        # normal page
        page = Canvas.objects.create(manifest=mfst, label='p. 33',
            short_id='page33', order=len(outside_views) + 1)
        # insertion
        insertion = Canvas.objects.create(manifest=mfst,
            label='pp. 33-34 Insertion A recto', short_id='insa',
            order=len(outside_views) + 2)

        overview_images = la_vie.overview_images()
        assert page not in overview_images
        assert insertion not in overview_images
        overview_labels = [c.label for c in overview_images]
        for label in outside_views:
            assert label in overview_labels

    def test_annotated_pages(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        # no digital edition - empty queryset
        assert la_vie.annotated_pages().count() == 0
        # digital edition, no pages
        la_vie.digital_edition = mfst = Manifest.objects.create(short_id='m1')
        assert la_vie.annotated_pages().count() == 0
        # normal pages, no annotations
        page = Canvas.objects.create(manifest=mfst, label='p. 33',
            short_id='page33', order=1)
        page2 = Canvas.objects.create(manifest=mfst, label='p. 35',
            short_id='page35', order=2)
        assert la_vie.annotated_pages().count() == 0
        # create an annotation
        Intervention.objects.create(canvas=page)
        assert la_vie.annotated_pages().count() == 1
        assert la_vie.annotated_pages().first() == page
        assert page2 not in la_vie.annotated_pages()
        # multiple annotations on the same page- should still only show once
        Intervention.objects.create(canvas=page)
        assert la_vie.annotated_pages().count() == 1

    def test_insertion_images(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        # no digital edition - empty queryset
        assert la_vie.insertion_images().count() == 0
        # digital edition, no pages
        la_vie.digital_edition = mfst = Manifest.objects.create(short_id='m1')
        assert la_vie.insertion_images().count() == 0
        # cover
        cover = Canvas.objects.create(manifest=mfst, label='Front Cover',
            short_id='cov1', order=1)
        # normal page
        page = Canvas.objects.create(manifest=mfst, label='p. 33',
            short_id='page33', order=2)
        # insertion
        insertion = Canvas.objects.create(manifest=mfst,
            label='pp. 33-34 Insertion A recto', short_id='insa', order=3)
        insertion2 = Canvas.objects.create(manifest=mfst,
            label='pp. 33-34 Insertion A verso', short_id='insb', order=4)

        insertions = la_vie.insertion_images()
        assert page not in insertions
        assert cover not in insertions
        assert insertion in insertions
        assert insertion2 in insertions

    def test_allow_canvas_detail(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        la_vie.digital_edition = mfst = Manifest.objects.create(short_id='m1')
        # cover
        cover = Canvas.objects.create(manifest=mfst, label='Front Cover',
            short_id='cov1', order=1)
        # normal page
        page = Canvas.objects.create(manifest=mfst, label='p. 33',
            short_id='page33', order=2)
        # insertion
        insertion = Canvas.objects.create(manifest=mfst,
            label='pp. 33-34 Insertion A recto', short_id='insa', order=3)

        assert Instance.allow_canvas_detail(cover)
        assert not Instance.allow_canvas_detail(page)
        assert Instance.allow_canvas_detail(insertion)

        Intervention.objects.create(canvas=page)
        assert Instance.allow_canvas_detail(page)

    def test_allow_canvas_large_image(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")
        la_vie.digital_edition = mfst = Manifest.objects.create(short_id='m1')
        # cover
        cover = Canvas.objects.create(manifest=mfst, label='Front Cover',
            short_id='cov1', order=1)
        # normal page
        page = Canvas.objects.create(manifest=mfst, label='p. 33',
            short_id='page33', order=2)
        # insertion
        insertion = Canvas.objects.create(manifest=mfst,
            label='pp. 33-34 Insertion A recto', short_id='insa', order=3)

        # insertion and overview always allowed
        assert la_vie.allow_canvas_large_image(cover)
        assert la_vie.allow_canvas_large_image(insertion)
        # unannotated page not allowed
        assert not la_vie.allow_canvas_large_image(page)

        # annotated page allowed if not suppressed
        Intervention.objects.create(canvas=page)
        assert la_vie.allow_canvas_large_image(page)

        # suppress all
        la_vie.suppress_all_images = True
        assert not la_vie.allow_canvas_large_image(page)

        # suppress a different page
        la_vie.suppress_all_images = False
        la_vie.suppressed_images.add(cover)
        assert la_vie.allow_canvas_large_image(page)

        # suppress this specific page
        la_vie.suppressed_images.add(page)
        assert not la_vie.allow_canvas_large_image(page)

    def test_related_instances(self):

        # get la_vie and clone it
        la_vie = Instance.objects.filter(work__primary_title__icontains='la vie').first()
        la_vie.digital_edition = mfst = Manifest.objects.create(short_id='m1')
        la_vie.save()
        pk = la_vie.pk
        la_vie.pk = None
        la_vie.digital_edition = mfst = Manifest.objects.create(short_id='m2')
        la_vie.slug = 'a-completely-different-slug'
        la_vie.save()
        # refresh the object so it has its pk and related objects
        la_vie.refresh_from_db()
        # original la_vie should be the only related instance
        assert len(la_vie.related_instances) == 1
        assert la_vie.related_instances[0].pk == pk
        # delete digital edition
        la_vie_old = la_vie.related_instances[0]
        la_vie_old.digital_edition = None
        la_vie_old.save()
        # now check to get an empty set
        la_vie.refresh_from_db()
        assert len(la_vie.related_instances) == 0


class TestInstanceQuerySet(TestCase):
    fixtures = ['sample_work_data.json']

    def setUp(self):
        self.manif1 = Manifest.objects.create(short_id='bk123', label='Foobar')

    def test_with_digital_eds(self):
        la_vie = Instance.objects.get(work__short_title__contains="La vie")

        # no digital editiosn with manifests, so should return empty queryset
        empty = Instance.objects.with_digital_eds()
        assert len(empty) == 0

        # associate la_vie with the set up manfest, len should be 1
        # and the only result should be la_vie
        la_vie.digital_edition = self.manif1
        la_vie.save()

        qs = Instance.objects.with_digital_eds()
        assert len(qs) == 1
        assert qs[0] == la_vie

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
