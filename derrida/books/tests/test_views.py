# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Min
from django.http import Http404
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.html import escape
from djiffy.models import Manifest, Canvas
import json
from haystack.models import SearchResult
import pytest

from derrida.books import views
from derrida.books.models import Instance, Reference, DerridaWorkSection
from derrida.interventions.models import Intervention, INTERVENTION_TYPES


#: override_settings and use test haystack connection
USE_TEST_HAYSTACK = override_settings(
    HAYSTACK_CONNECTIONS=settings.HAYSTACK_TEST_CONNECTIONS)


@USE_TEST_HAYSTACK
class TestInstanceViews(TestCase):
    fixtures = ['test_instances.json']

    def test_instance_detail_view(self):
        # get an instance of la_vie
        la_vie = Instance.objects.filter(work__primary_title__icontains='la vie').first()
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

    @pytest.mark.haystack
    def test_instance_list_view(self):
        list_view_url = reverse('books:list')
        # an anonymous user can see the view
        response = self.client.get(list_view_url)

        extant_bks = Instance.objects.filter(is_extant=True,
            journal__isnull=True, collected_in__isnull=True)

        assert response.status_code == 200
        # an object list is returned
        assert 'object_list' in response.context
        # Should find 16 objects and a paginator in context
        assert len(response.context['object_list']) == 16

        extant_bks = Instance.objects.filter(is_extant=True,
            journal__isnull=True, collected_in__isnull=True)
        # 19 extant books in the fixture (excludes non-extant and book section)
        assert response.context['total'] == extant_bks.count()
        # facets should be set
        assert response.context['facets']
        self.assertContains(response, '19 Results',
            msg_prefix='total number of results displayed')
        assert isinstance(response.context['object_list'][0], SearchResult)
        assert response.context['object_list'][0].model == Instance
        assert 'page_obj' in response.context
        page_obj = response.context['page_obj']
        assert page_obj
        # Paginator 1 indexes this rather than 0, it's 2 pages!
        assert page_obj.paginator.page_range == range(1, 3)
        assert page_obj.number == 1

        # load a different page
        response = self.client.get(list_view_url, {'page': 2})

        assert response.status_code == 200
        page_obj = response.context['page_obj']
        assert page_obj
        assert page_obj.paginator.page_range == range(1, 3)
        assert page_obj.number == 2
        # only 3 items on pg. 2
        assert len(response.context['object_list']) == 3

        # test search/facet/order by
        response = self.client.get(list_view_url, {'query': 'anthropologie'})
        assert response.context['object_list'][0].display_title == \
            "Anthropologie structurale"
        # sort
        response = self.client.get(list_view_url, {'order_by': 'title'})
        assert response.context['object_list'][0].display_title == \
            'A Study of Writing'
        # annotated only
        response = self.client.get(list_view_url, {'is_annotated': True})
        assert len(response.context['object_list']) == \
            extant_bks.filter(is_annotated=True).count()
        # multiple facets should return both
        response = self.client.get(list_view_url, {'pub_place': ['Paris', 'Pfullingen']})
        # fixture has 12 published in Paris and 1 in Pfulligen
        assert len(response.context['object_list']) == 14

        # search for non-cited volume
        response = self.client.get(list_view_url, {'query': 'gelb'})
        # should not be found
        assert len(response.context['object_list']) == 0

    def test_canvas_by_pagenum(self):
        # get an instance with no digital edition
        item = Instance.objects.filter(digital_edition__isnull=True).first()
        canvas_page_url = reverse('books:canvas-by-page',
            kwargs={'slug': item.slug, 'page_num': '23'})
        response = self.client.get(canvas_page_url)
        # no digital edition - should 404
        assert response.status_code == 404

        # get an instance with a digital edition
        item = Instance.objects.filter(digital_edition__isnull=False).first()
        canvas_page_url = reverse('books:canvas-by-page',
            kwargs={'slug': item.slug, 'page_num': '23'})
        response = self.client.get(canvas_page_url)
        # digital edition has no canvases - should still 404
        assert response.status_code == 404

        # create a canvas with matching label
        canvas = Canvas.objects.create(manifest=item.digital_edition, order=1,
            label='p. 23', short_id='c00123')
        response = self.client.get(canvas_page_url)
        assert response.status_code == 303
        canvas_image_url = reverse('books:canvas-image',
            kwargs={'slug': item.slug, 'short_id': canvas.short_id,
                    'mode': 'thumbnail'})
        assert response.url == canvas_image_url

        # variant page numbers and page ranges should all work
        # - page range
        canvas_page_url = reverse('books:canvas-by-page',
            kwargs={'slug': item.slug, 'page_num': '23-24'})
        response = self.client.get(canvas_page_url)
        assert response.url == canvas_image_url
        # - some reference pages currently have an extra letter
        canvas_page_url = reverse('books:canvas-by-page',
            kwargs={'slug': item.slug, 'page_num': '23p'})
        response = self.client.get(canvas_page_url)
        assert response.url == canvas_image_url
        # - other extra characters
        canvas_page_url = reverse('books:canvas-by-page',
            kwargs={'slug': item.slug, 'page_num': '23s'})
        response = self.client.get(canvas_page_url)
        assert response.url == canvas_image_url
        # page range + character
        canvas_page_url = reverse('books:canvas-by-page',
            kwargs={'slug': item.slug, 'page_num': '23-24p'})
        response = self.client.get(canvas_page_url)
        assert response.url == canvas_image_url

        # if no match for page, should fallback to item thumbnail
        cover = Canvas.objects.create(manifest=item.digital_edition, order=2,
            label='Front Cover', short_id='cover1', thumbnail=True)
        canvas_page_url = reverse('books:canvas-by-page',
            kwargs={'slug': item.slug, 'page_num': '1234'})
        response = self.client.get(canvas_page_url)
        cover_image_url = reverse('books:canvas-image',
            kwargs={'slug': item.slug, 'short_id': cover.short_id,
                    'mode': 'thumbnail'})
        assert response.url == cover_image_url

    def test_canvas_detail_view(self):
        # get an instance with a digital edition
        item = Instance.objects.filter(digital_edition__isnull=False).first()
        # add logo and license to manifest
        item.digital_edition.extra_data['logo'] = 'http://so.me/logo.img'
        item.digital_edition.extra_data['license'] = 'http://rightsstatements.org/page/InC/1.0/'
        item.digital_edition.save()

        # create some test canvases
        cover = Canvas.objects.create(manifest=item.digital_edition, order=2,
            label='Front Cover', short_id='cover1')
        cover2 = Canvas.objects.create(manifest=item.digital_edition, order=3,
            label='Inside Front Cover', short_id='cover2')
        p23 = Canvas.objects.create(manifest=item.digital_edition, order=4,
            label='p. 23', short_id='p23')
        ins = Canvas.objects.create(manifest=item.digital_edition, order=5,
            label='pp. 20-21 Insertion A recto', short_id='ins1')

        cover_detail_url = reverse('books:canvas-detail',
            kwargs={'slug': item.slug, 'short_id': cover.short_id})
        response = self.client.get(cover_detail_url)
        self.assertContains(response, cover.label)
        self.assertContains(response, item.display_title())
        # includes larger page image url
        self.assertContains(response, reverse('books:canvas-image',
            kwargs={'slug': item.slug, 'short_id': cover.short_id,
                'mode': 'large'}))
        # includes image info url for deep zoom
        self.assertContains(response, reverse('books:canvas-image',
            kwargs={'slug': item.slug, 'short_id': cover.short_id,
                'mode': 'info'}))
        # includes nav to other viewable pages
        for page in [cover2, ins]:
            self.assertContains(response, page.label)
            self.assertContains(response, reverse('books:canvas-detail',
                kwargs={'slug': item.slug, 'short_id': page.short_id}))
        # unannotated page not listed in nav
        p23_detail_url = reverse('books:canvas-detail',
            kwargs={'slug': item.slug, 'short_id': p23.short_id})
        self.assertNotContains(response, p23.label)
        self.assertNotContains(response, p23_detail_url)
        # includes brief list of locations cited by Derrida
        for ref in item.reference_set.all():
            self.assertContains(response,
                'p.%s %s' % (ref.derridawork_page, ref.derridawork_pageloc))
        # iiif logo and license should be present somewhere
        self.assertContains(response, item.digital_edition.logo)
        self.assertContains(response, item.digital_edition.license)

        # trying to get normal page with no annotations should fail
        response = self.client.get(p23_detail_url)
        assert response.status_code == 404

        # add an intervention to p23 - should now succeed
        Intervention.objects.create(canvas=p23)
        response = self.client.get(p23_detail_url)
        assert response.status_code == 200

        # annotated page should be listed in nav on other pages
        response = self.client.get(cover_detail_url)
        self.assertContains(response, p23.label)
        self.assertContains(response, p23_detail_url)

        # should not include suppress canvas form (non-admin)
        suppress_url = reverse('books:suppress-canvas', kwargs={'slug': item.slug})
        self.assertNotContains(response, suppress_url)

        # login as admin with change_instance permission
        pword = 'testing123'
        content_admin = get_user_model().objects.create_user('testeditor',
            'test@example.com', pword)
        content_admin.user_permissions.add(
            Permission.objects.get(codename='change_instance',
                content_type=ContentType.objects.get(app_label='books',
                                                     model='instance'))
        )
        self.client.login(username=content_admin.username, password=pword)
        response = self.client.get(cover_detail_url)
        # form should be displayed
        self.assertContains(response, suppress_url)
        # current canvas id set as hidden input
        self.assertContains(response,
            '<input type="hidden" name="canvas_id" value="%s" id="id_canvas_id"/>' % \
              cover.short_id, html=True)

        # if item is suppressed, form is not displayed
        item.suppressed_images.add(cover)
        response = self.client.get(cover_detail_url)
        assert response.context['canvas_suppressed']
        self.assertNotContains(response, suppress_url)
        self.assertContains(response, 'This page image is suppressed')

        item.suppressed_images.remove(cover)
        item.suppress_all_images = True
        item.save()
        response = self.client.get(cover_detail_url)
        assert response.context['canvas_suppressed']
        self.assertNotContains(response, suppress_url)
        self.assertContains(response,
            'All annotated page images in this volume are suppressed.')

        # anonymous user does not see warning, but suppress flag
        # is set in context to aid with display
        self.client.logout()
        response = self.client.get(cover_detail_url)
        assert response.context['canvas_suppressed']
        self.assertNotContains(response,
            'All annotated page images in this volume are suppressed.')

    def test_canvas_suppress_view(self):
        # get an instance with a digital edition
        item = Instance.objects.filter(digital_edition__isnull=False).first()
        # create test canvas
        p23 = Canvas.objects.create(manifest=item.digital_edition, order=4,
            label='p. 23', short_id='p23')

        suppress_url = reverse('books:suppress-canvas', kwargs={'slug': item.slug})
        # insufficent perms
        # get redirects
        response = self.client.get(suppress_url)
        # by default, django redirects user to login if permission check fails
        assert response.status_code == 302
        assert 'accounts/login' in response.url

        # login as admin with change_instance permission
        pword = 'testing123'
        content_admin = get_user_model().objects.create_user('testeditor',
            'test@example.com', pword)
        content_admin.user_permissions.add(
            Permission.objects.get(codename='change_instance',
                content_type=ContentType.objects.get(app_label='books',
                                                     model='instance'))
        )
        self.client.login(username=content_admin.username, password=pword)

        # get redirects to book detail
        response = self.client.get(suppress_url)
        assert response.status_code == 303
        assert response.url == reverse('books:detail', kwargs={'slug': item.slug})

        # post should process the request
        response = self.client.post(suppress_url,
            {'suppress': 'current', 'canvas_id': p23.short_id})
        assert response.status_code == 303
        assert response.url == reverse('books:canvas-detail',
            kwargs={'slug': item.slug, 'short_id': p23.short_id})

        # canvas is now suppressed
        assert p23 in item.suppressed_images.all()
        # TODO: check that messages are set?

        # post should process the request
        response = self.client.post(suppress_url,
            {'suppress': 'all', 'canvas_id': p23.short_id})

        # get fresh copy of item from db
        item = Instance.objects.get(pk=item.pk)
        assert item.suppress_all_images


@USE_TEST_HAYSTACK
class TestReferenceViews(TestCase):
    fixtures = ['test_references.json']

    def setUp(self):
        '''None of the Instacefixtures have slugs, so generate them'''
        for instance in Instance.objects.all():
            instance.slug = instance.generate_safe_slug()
            instance.save()

    @pytest.mark.haystack
    def test_reference_list(self):
        reference_list_url = reverse('books:reference-list')
        response = self.client.get(reference_list_url)
        assert response.status_code == 200
        assert 'object_list' in response.context
        assert isinstance(response.context['object_list'][0], SearchResult)
        assert response.context['object_list'][0].model == Reference
        self.assertTemplateUsed(response, 'books/reference_list.html')
        self.assertTemplateUsed(response, 'components/citation-list-item.html')
        self.assertTemplateUsed(response, 'components/page-pagination.html')

        # total number of matches should be set in context and displayed
        assert response.context['total'] == 20
        self.assertContains(response, '20 Results',
            msg_prefix='total number of results displayed')

        # reference details that should be present in the template
        ref = Reference.objects.first()
        # spot check template (tested more thoroughly in reference detail below)
        self.assertContains(response, 'p. %s' % ref.book_page,
            msg_prefix='reference detail should include book page number')
        self.assertContains(response, escape(ref.instance.display_title()),
            msg_prefix='reference detail should include book title')
        # default sort is derrida work page
        ref = Reference.objects.order_by('derridawork_page').first()
        first_ref = response.context['object_list'][0]
        assert (ref.derridawork_page, ref.derridawork_pageloc) == \
            (first_ref.derridawork_page, first_ref.derridawork_pageloc)

        # pagination: link to page two
        # will eventually need to include sort/filter options
        self.assertContains(response, '?page=2',
            msg_prefix='should include link to next page of results')

        # test results filtered by type
        response = self.client.get(reference_list_url,
            {'reference_type': 'Epigraph'})  # 15 epigraphs in fixture
        assert response.status_code == 200
        # not enough results to paginate
        self.assertTemplateNotUsed(response, 'components/page-pagination.html')

        # keyword search
        response = self.client.get(reference_list_url, {'query': 'lettres'})
        # anchor text for matching reference should display
        assert response.status_code == 200
        assert len(response.context['object_list']) == 1
        self.assertContains(response,
            escape("alphabet, de la syllabation"),
            msg_prefix='should include anchor text for matching reference')
        self.assertContains(response, '<em>Grammatologie</em>',
            msg_prefix='markdown formatting in anchor text should be rendered as html')

        # test no results displayed
        response = self.client.get(reference_list_url, {'query': 'foobar'})
        assert len(response.context['object_list']) == 0
        self.assertContains(response,
            'No trace of what you were searching for was found')

        # filter by is extant
        response = self.client.get(reference_list_url, {'is_extant': 'on'})
        assert len(response.context['object_list']) == \
            Reference.objects.filter(instance__is_extant=True).count()

        # filter by is annotated
        response = self.client.get(reference_list_url, {'is_annotated': 'on'})
        assert len(response.context['object_list']) == \
            Reference.objects.filter(instance__is_annotated=True).count()

        # facet filter on multiple authors
        authors = ['Granger, Gilles-Gaston', 'Nietzsche, Friedrich']
        response = self.client.get(reference_list_url, {'author': authors})
        assert len(response.context['object_list']) == \
            Reference.objects.filter(instance__work__authors__authorized_name__in=authors).count()

        # sort by cited item title
        response = self.client.get(reference_list_url, {'order_by': 'cited_title'})
        ref = Reference.objects.order_by('instance__work__short_title').first()
        first_ref = response.context['object_list'][0]
        assert ref.instance.display_title() == first_ref.instance_title

        # filter by corresponding annotation
        response = self.client.get(reference_list_url, {'corresponding_intervention': 'on'})
        assert len(response.context['object_list']) == 1

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
        self.assertNotContains(response,
            'p.%s %s' % (ref.derridawork_page, ref.derridawork_pageloc),
            msg_prefix='should not include Derrida work page with page location')
        self.assertContains(response, 'p.%s' % ref.derridawork_page,
            msg_prefix='should include Derrida work page')

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


class TestCanvasImageView(TestCase):
    fixtures = ['sample_work_data.json']

    def test_get_proxy_url(self):
        # setup an instance with some test canvases
        item = Instance.objects.all().first()
        manif = Manifest.objects.create()
        item.digital_edition = manif
        item.save()

        cover = Canvas.objects.create(manifest=item.digital_edition, order=2,
            label='Front Cover', short_id='cover1',
            iiif_image_id='http://ima.ge/c1')
        cover2 = Canvas.objects.create(manifest=item.digital_edition, order=3,
            label='Inside Front Cover', short_id='cover2',
            iiif_image_id='http://ima.ge/c2')
        p23 = Canvas.objects.create(manifest=item.digital_edition, order=4,
            label='p. 23', short_id='p23', iiif_image_id='http://ima.ge/p1')
        p24 = Canvas.objects.create(manifest=item.digital_edition, order=5,
            label='p. 24', short_id='p24', iiif_image_id='http://ima.ge/p2')
        ins = Canvas.objects.create(manifest=item.digital_edition, order=6,
            label='pp. 20-21 Insertion A recto', short_id='ins1',
            iiif_image_id='http://ima.ge/i1')
        # add an intervention to p23 - should now succeed
        Intervention.objects.create(canvas=p23)

        canvasimgview = views.CanvasImage()

        canvasimgview.kwargs = {'slug': item.slug, 'short_id': cover.short_id}
        imgurl = canvasimgview.get_proxy_url(mode='thumbnail')
        assert str(imgurl) == str(cover.image.thumbnail())
        imgurl = canvasimgview.get_proxy_url(mode='large')
        assert str(imgurl) == str(cover.image.size(height=850, width=850,
            exact=True))
        imgurl = canvasimgview.get_proxy_url(mode='info')
        assert str(imgurl) == str(cover.image.info())

        # sample iiif image tile used for deep zooom
        iiif_url = '0,0,2048,2048/1024,/0/default.jpg'
        imgurl = canvasimgview.get_proxy_url(mode='iiif', url=iiif_url)
        assert str(imgurl) == str(cover.image \
                .region(x=0, y=0, width=2048, height=2048).size(width=1024))

        # large image restricted to certain images only
        # - overview image
        canvasimgview.kwargs['short_id'] = cover2.short_id
        imgurl = canvasimgview.get_proxy_url(mode='large')
        assert str(imgurl) == str(cover2.image.size(height=850, width=850,
            exact=True))
        # - insertion image
        canvasimgview.kwargs['short_id'] = ins.short_id
        imgurl = canvasimgview.get_proxy_url(mode='large')
        assert str(imgurl) == str(ins.image.size(height=850, width=850,
            exact=True))
        # page with interventions
        canvasimgview.kwargs['short_id'] = p23.short_id
        imgurl = canvasimgview.get_proxy_url(mode='large')
        assert str(imgurl) == str(p23.image.size(height=850, width=850,
            exact=True))
        # page without interventions should 40
        with pytest.raises(Http404):
            canvasimgview.kwargs['short_id'] = p24.short_id
            canvasimgview.get_proxy_url(mode='large')


    # TODO: test proxyview logic in preserving headers, rewriting
    # iiif id to local url, etc