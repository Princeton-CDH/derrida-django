# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.db.models import Min, Q
from django.db.transaction import atomic
from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape
from djiffy.models import Manifest
import json

from derrida.people.models import Person
from derrida.books.models import Instance, Work, Reference, DerridaWorkSection
from derrida.interventions.models import Intervention, INTERVENTION_TYPES


class TestInstanceViews(TestCase):
    fixtures = ['sample_work_data.json']

    def setUp(self):
        la_vie = Instance.objects.get(work__primary_title__icontains='la vie')
        for i in range(1, 20):
            la_vie.pk = None
            la_vie.save()

    def test_instance_detail_view(self):
        # get one of the la_vie copies
        la_vie = Instance.objects.filter(work__primary_title__icontains='la vie')[3]
        # pass its pk to detail view
        detail_view_url = la_vie.get_absolute_url()
        response = self.client.get(detail_view_url)
        # doesn't have a manifest, should 404
        # should return a response
        assert response.status_code == 404

        # make a manifest and associate it
        manif = Manifest.objects.create()
        la_vie.digital_edition = manif
        la_vie.save()

        response = self.client.get(detail_view_url)
        # should return correctly
        assert response.status_code == 200
        # should have a context object called instance that's a copy of Instance
        assert 'instance' in response.context
        # it should be the copy of la_view we looked up
        assert response.context['instance'] == la_vie

    def test_instance_list_view(self):
        list_view_url = reverse('books:list')
        # an anonymous user can see the view
        response = self.client.get(list_view_url)
        assert response.status_code == 200
        # an object list is returned
        assert 'object_list' in response.context
        # Should find 16 objects and a paginator in context
        assert len(response.context['object_list']) == 16
        assert 'page_obj' in response.context
        page_obj = response.context['page_obj']
        assert page_obj
        # Paginator 1 indexes this rather than 0, it's 2 pages!
        assert page_obj.paginator.page_range == range(1, 3)
        assert page_obj.number == 1

        # - testing that query set is alpha by author of work
        # Make one more work, and give it an author
        testwork = Work.objects.create(
            primary_title="Un livre d'unittest",
            short_title="Un livre"
        )
        # author starts with 'a' so it should come first
        pers = Person.objects.create(authorized_name='Adespota', birth=1800,
            death=1845)
        testwork.authors.add(pers)
        testwork.save()
        # make an instance from that work
        inst = Instance.objects.create(work=testwork)
        # check the context to ensure it is there and firstß
        response = self.client.get(list_view_url)
        assert response.status_code == 200
        assert 'object_list' in response.context
        assert response.context['object_list'][0] == inst
        # still 16 items
        assert len(response.context['object_list']) == 16
        # still page 1
        page_obj = response.context['page_obj']
        assert page_obj
        assert page_obj.paginator.page_range == range(1, 3)
        assert page_obj.number == 1
        # now pick a different page via query string
        response = self.client.get(list_view_url, {'page': 2})
        assert response.status_code == 200
        page_obj = response.context['page_obj']
        assert page_obj
        assert page_obj.paginator.page_range == range(1, 3)
        assert page_obj.number == 2
        # only 5 of 21 items on pg. 2
        assert len(response.context['object_list']) == 5


class TestReferenceViews(TestCase):
    fixtures = ['test_references.json']


    def setUp(self):
        '''None of the Instacefixtures have slugs, so generate them'''
        for instance in Instance.objects.all():
            instance.slug = instance.generate_safe_slug()
            instance.save()

    def test_reference_list(self):
        reference_list_url = reverse('books:reference-list')
        response = self.client.get(reference_list_url)
        assert response.status_code == 200
        assert 'object_list' in response.context
        assert isinstance(response.context['object_list'][0], Reference)
        self.assertTemplateUsed(response, 'books/reference_list.html')
        self.assertTemplateUsed(response, 'components/citation-list-item.html')
        self.assertTemplateUsed(response, 'components/page-pagination.html')

        # fixme: is total displayed anywhere?

        # reference details that should be present in the template
        ref = Reference.objects.first()
        # spot check template (tested more thoroughly in reference detail below)
        self.assertContains(response, 'p. %s' % ref.book_page,
            msg_prefix='reference detail should include book page number')
        self.assertContains(response, escape(ref.instance.display_title()),
            msg_prefix='reference detail should include book title')

        # pagination: link to page two
        # FIXME: should this include current page url?
        # will eventually need to include sort/filter options
        self.assertContains(response, '?page=2',
            msg_prefix='should include link to next page of results')

        # test non-paginated results
        # - remove all but five references
        keep_ids = Reference.objects.values_list('id', flat=True)[:5]
        # MySQL can't handle exclude in list (LIMIT & IN/ALL/ANY/SOME subquery)
        # So use an OR Query to remove all but the ids we want to keep
        id_query = Q()
        for ref_id in keep_ids:
            id_query |= Q(id=ref_id)
        Reference.objects.exclude(id_query).delete()

        response = self.client.get(reference_list_url)
        assert response.status_code == 200
        self.assertTemplateNotUsed(response, 'components/page-pagination.html')

        # todo: test no results display?

    def test_reference_detail(self):
        ref = Reference.objects.exclude(book_page='').first()
        response = self.client.get(ref.get_absolute_url())
        assert response.status_code == 200
        self.assertTemplateUsed('components/citation-list-item.html')
        # check for details that should be displayed
        # - reference type
        self.assertContains(response, ref.reference_type.name,
            msg_prefix='should display reference type')
        # - link to cited book
        self.assertContains(response, ref.instance.get_absolute_url(),
            msg_prefix='should include link to work instance detail page')
        # - cited book title
        self.assertContains(response, escape(ref.instance.display_title()),
            msg_prefix='should include work instance title')
        # - work instance authors
        self.assertContains(response,
            '; '.join([a.authorized_name for a in ref.instance.work.authors.all()]),
            msg_prefix='should display all author names')
        # - instance copyright year
        self.assertContains(response, ref.instance.copyright_year,
            msg_prefix='should include work instance copyright year')
        # - reference page number
        self.assertContains(response, 'p. %s' % ref.book_page,
            msg_prefix='should include reference page number')
        # - reference anchor text
        self.assertContains(response, ref.anchor_text,
            msg_prefix='should include reference anchor text')
        # - derrida work citation
        self.assertContains(response, ref.derridawork,
            msg_prefix='should include Derrida work title')
        self.assertContains(response,
            'p.%s %s' % (ref.derridawork_page, ref.derridawork_pageloc),
            msg_prefix='should include Derrida work location')

        # display for page range
        ref.book_page = '100-101'
        ref.save()
        response = self.client.get(ref.get_absolute_url())
        self.assertContains(response, 'pp. %s' % ref.book_page,
            msg_prefix='display reference page number with pp. for ranges')

    def test_reference_histogram(self):
        # default: reference by author of referenced book
        histogram_url = reverse('books:reference-histogram')
        response = self.client.get(histogram_url)
        self.assertTemplateUsed(response, 'books/reference_histogram.html')
        assert list(response.context['object_list']) == \
            list(Reference.objects.order_by_author().summary_values())
        assert 'sections' not in response.context
        refs = Reference.objects.all()
        for ref in refs:
            self.assertContains(response, ref.get_absolute_url(),
                msg_prefix='template should include link to reference')
            self.assertContains(response, ref.instance.get_absolute_url(),
                msg_prefix='template should include link to cited item')

        authors = [ref.instance.work.authors.first().authorized_name if ref.instance.work.authors.first()    else None
                   for ref in refs]
        for auth in authors:
            self.assertContains(response, auth or '[no author]', count=1,
                msg_prefix='template should include each referenced author once')

        dg = Reference.objects.first().derridawork
        histogram_url = reverse('books:reference-histogram',
            kwargs={'derridawork_slug': dg.slug})
        response = self.client.get(histogram_url)
        assert list(response.context['object_list']) == \
            list(Reference.objects.order_by_source_page().summary_values())
        assert response.context['mode'] == 'section'
        sections = DerridaWorkSection.objects.filter(derridawork__slug=dg.slug)
        assert list(response.context['sections']) == list(sections)

        for sect in sections:
            self.assertContains(response, escape(sect.name),
                msg_prefix='section label should be displayed when viewing citations by chapter')

        # exclude any references lower than first section start page
        min_startpage = sections.aggregate(Min('start_page'))['start_page__min']
        refs = Reference.objects.filter(derridawork__slug=dg.slug,
                                        derridawork_page__gt=min_startpage)
        for ref in refs:
            self.assertContains(response, ref.get_absolute_url(),
                msg_prefix='template should include link to reference')
            self.assertContains(response, ref.instance.get_absolute_url(),
                msg_prefix='template should include link to cited item')


class TestBookViews(TestCase):
    fixtures = ['sample_work_data.json', 'test_canvas_data.json']

    def setUp(self):
        # create an admin user to test autocomplete views
        self.password = 'pass!@#$'
        self.admin = get_user_model().objects.create_superuser('testadmin',
            'test@example.com', self.password)

    def test_publisher_autocomplete(self):
        # Not accessible to anonymous user
        pub_autocomplete_url = reverse('books:publisher-autocomplete')
        response = self.client.get(pub_autocomplete_url)
        assert response.status_code == 302

        # Get a response as a staff user
        self.client.login(username=self.admin.username, password=self.password)
        response = self.client.get(pub_autocomplete_url, params={'q': 'Bacon'})
        assert response.status_code == 200
        data = json.loads(response.content.decode('utf-8'))
        assert 'results' in data
        assert data['results'][0]['text'] == 'Baconnière'

    def test_language_autocomplete(self):
        # Not accessible to anonymous user
        lang_autocomplete_url = reverse('books:language-autocomplete')
        response = self.client.get(lang_autocomplete_url)
        assert response.status_code == 302

        # Get a response as a staff user
        self.client.login(username=self.admin.username, password=self.password)
        response = self.client.get(lang_autocomplete_url, params={'q': 'eng'})
        assert response.status_code == 200
        data = json.loads(response.content.decode('utf-8'))
        assert 'results' in data
        assert data['results'][0]['text'] == 'English'

    def test_instance_admin_editform(self):
        self.client.login(username=self.admin.username, password=self.password)
        inst = Instance.objects.first()
        instance_edit_url = reverse('admin:books_instance_change',
            args=[inst.id])
        response = self.client.get(instance_edit_url)
        # with no interventions, just test that the view renders
        assert response.status_code == 200

        # associate library instance with a digital edition
        manif = Manifest.objects.first()
        inst.digital_edition = manif
        inst.save()
        cnvs1, cnvs2 = manif.canvases.first(), manif.canvases.last()
        # add test interventions to canvases associated with the manifest
        ivtns = Intervention.objects.bulk_create([
            # annotation on canvas 1, no text
            Intervention(uri=cnvs1.uri, canvas=cnvs1,
                intervention_type=INTERVENTION_TYPES.ANNOTATION),
            # annotation on canvas 2 with text
            Intervention(uri=cnvs2.uri, canvas=cnvs2,
                intervention_type=INTERVENTION_TYPES.ANNOTATION,
                text='Some annotation comment here'),
            # insertion on canvas 2 with text
            Intervention(uri=cnvs2, canvas=cnvs2,
                intervention_type=INTERVENTION_TYPES.INSERTION,
                text='A different insertion comment here'),
        ])
        response = self.client.get(instance_edit_url)
        self.assertTemplateUsed(template_name='admin/books/instance/change_form.html')

        self.assertContains(response, cnvs1.label, count=1,
            msg_prefix='canvas label should appear once for each associated intervention')
        self.assertContains(response, cnvs2.label, count=2,
            msg_prefix='canvas label should appear once for each associated intervention')
        self.assertContains(response, cnvs1.get_absolute_url(), count=1,
            msg_prefix='canvas url should be included once for each associated intervention')
        self.assertContains(response, cnvs2.get_absolute_url(), count=2,
            msg_prefix='canvas url should be included once for each associated intervention')
        self.assertContains(response, 'Annotation', count=2,
            msg_prefix='intervention type should display for each item')
        self.assertContains(response, 'Intervention', count=5,
            msg_prefix='intervention type should display for each item, once in'
            ' the reference inline, and once in the hidden reference inline, and'
            ' the inline fieldset.')

        for intervention in ivtns:
            self.assertContains(response, intervention.admin_thumbnail(),
                msg_prefix='should display admin thumbnail for each intervention')
            self.assertContains(response, intervention.text_preview(),
                msg_prefix='should display text preview for each intervention')
            self.assertContains(response,
                reverse('admin:interventions_intervention_change', args=[intervention.id]),
                msg_prefix='should link to intervention edit page')
