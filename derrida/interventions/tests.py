# -*- coding: utf-8 -*-
import datetime
import json
from unittest.mock import Mock, patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.db.models import Max, Min
from django.test import TestCase, override_settings
from django.urls import reverse
from djiffy.models import Canvas, Manifest
from haystack.models import SearchResult
import pytest

from derrida.books.models import Instance, Language
from derrida.people.models import Person
from .models import Tag, INTERVENTION_TYPES, Intervention, get_default_intervener


class TestTagQuerySet(TestCase):

    #  test custom queryset filters based on initial set of preloaded tags

    def test_qs_for_annotations(self):
        # create insertion-only tag for testing
        Tag.objects.create(name='post-it note',
            applies_to=INTERVENTION_TYPES.INSERTION)

        annotation_tags = Tag.objects.for_annotations()
        # annotation only tag
        assert annotation_tags.filter(name='underlining').exists()
        # annotation/insertion tag
        assert annotation_tags.filter(name='transcription uncertain').exists()
        # insertion only
        assert not annotation_tags.filter(name='post-it note').exists()

    def test_qs_for_insertions(self):
        # create insertion-only tag for testing
        Tag.objects.create(name='post-it note',
            applies_to=INTERVENTION_TYPES.INSERTION)

        insertion_tags = Tag.objects.for_insertions()
        # annotation only tag
        assert not insertion_tags.filter(name='underlining').exists()
        # annotation/insertion tag
        assert insertion_tags.filter(name='transcription uncertain').exists()
        # insertion only
        assert insertion_tags.filter(name='post-it note').exists()


class TestIntervention(TestCase):

    # def setUp(self):
        #         # create a person we can use for all the tests
        # book = Book.objects.create(title='Long title', short_title='Long',
        #     original_pub_info='fake pub info')
        # self.author = Person.objects.create(authorized_name='Bar, Foo')
        # self.pb = PersonBook.objects.create(book=book, person=self.author,
        #     relationship_type=PersonBookRelationshipType.objects.get(pk=1))

    def test_str(self):
        # canvas automatically associated by uri on save
        manif = Manifest.objects.create()
        canvas = Canvas.objects.create(uri='http://so.me/iiif/id/',
            order=0, manifest=manif, label='foo')
        note = Intervention.objects.create(uri=canvas.uri)
        # Minimum possible information, canvas
        assert str(note) == 'Annotation with no text (foo)'
        note.tags.set(Tag.objects.filter(name__in=['underlining', 'arrow']))
        # Add tags
        assert str(note) == ('Annotation with no text, tagged as '
                             'arrow, underlining (foo)')
        # Add text
        note.text = 'text'
        assert str(note) == 'text (foo)'
        # Add quote
        note.quote = 'quote'
        assert str(note) == 'quote (foo)'

    def test_save(self):
        # canvas automatically associated by uri on save
        manif = Manifest.objects.create()
        canvas = Canvas.objects.create(uri='http://so.me/iiif/id/',
            order=0, manifest=manif)
        note = Intervention.objects.create(uri=canvas.uri)
        assert note.canvas == canvas

        # check that canvas db lookup is skipped when not needed
        with patch('derrida.interventions.models.Canvas') as mockcanvas:
            mockcanvas.DoesNotExist = Canvas.DoesNotExist
            note.save()
            mockcanvas.objects.get.assert_not_called()

            # if uri changes, canvas should be cleared
            mockcanvas.objects.get.side_effect = Canvas.DoesNotExist
            note.uri = 'http://some.thing/else'
            note.save()
            assert not note.canvas
            mockcanvas.objects.get.assert_called_with(uri=note.uri)

    def test_handle_extra_data(self):
        # Create a blank, unsaved intervention object
        # (unsaved to check that handle_extra_data calls save if nececsary
        # before attempting to add foreign key associations)

        note = Intervention()

        ### tags ###

        # test adding new tags
        # - using three existing tags and one nonexistent
        tags = ['underlining', 'circling', 'bogus']
        data = note.handle_extra_data({'tags': tags},
            Mock())   # NOTE: using Mock() for request - currently unused
        # existing tags should be associated with annotation
        assert note.tags.count() == 2
        saved_tags = [tag.name for tag in note.tags.all()]
        for tag in tags[:-1]:
            assert tag in saved_tags
        # bogus tag should be ignored
        assert 'bogus' not in saved_tags
        # tags should be removed from annotation extra data
        assert 'tags' not in data

        # test changing the list of existing tags
        tags = ['circling']
        note.handle_extra_data({'tags': tags}, Mock())
        assert note.tags.count() == 1
        # underlining should be removed
        saved_tags = [tag.name for tag in note.tags.all()]
        assert 'underlining' not in saved_tags

        # test removing existing tags
        note.handle_extra_data({'tags': []}, Mock())
        assert note.tags.count() == 0

        ### languages ###

        # test setting text language
        # - valid language name
        data = note.handle_extra_data({'text_language': 'English'}, Mock())
        assert note.text_language.name == 'English'
        assert 'text_language' not in data
        # - invalid language name does not error, clears language
        data = note.handle_extra_data({'text_language': 'Klingon'}, Mock())
        assert note.text_language is None
        # - empty language does not error, clears out
        note.text_language = Language.objects.first()
        data = note.handle_extra_data({'text_language': ''}, Mock())
        assert note.text_language is None
        # value not present is also not an error
        note.language = Language.objects.first()
        data = note.handle_extra_data({}, Mock())
        assert note.text_language is None

        # test setting quoted text / anchor text language
        # - valid language name
        data = note.handle_extra_data({'quote_language': 'English'}, Mock())
        assert note.quote_language.name == 'English'
        assert 'quote_language' not in data
        # - invalid language name does not error, clears language
        data = note.handle_extra_data({'quote_language': 'Klingon'}, Mock())
        assert note.quote_language is None
        # - empty language does not error, clears out
        note.quote_language = Language.objects.first()
        data = note.handle_extra_data({'quote_language': ''}, Mock())
        assert note.quote_language is None
        # value not present is also not an error
        note.language = Language.objects.first()
        data = note.handle_extra_data({}, Mock())
        assert note.quote_language is None

        ### text translation ###
        translation_text = 'translated text goes here'
        data = note.handle_extra_data({'text_translation': translation_text},
            Mock())
        assert 'text_translation' not in data
        assert note.text_translation == translation_text
        note.handle_extra_data({}, Mock())
        assert note.text_translation == ''

        ### author ###
        author = Person.objects.create(authorized_name='Derrida, Jacques')
        # - if authorized_name matches, set
        data = note.handle_extra_data({'author': author.authorized_name}, Mock())
        assert note.author == author
        # - if 'author' not in data, unset
        data = note.handle_extra_data({}, Mock())
        assert not note.author

    def test_info(self):
        note = Intervention.objects.create()

        # tags should be an empty list when none are set
        assert not note.info()['tags']
        tags = ['circling', 'arrow']
        note.handle_extra_data({'tags': tags}, Mock())
        # order not guaranteed / not important; compare as a set
        assert set(note.info()['tags']) == set(tags)

        # languages should be present if set
        # not set - not included in info
        info = note.info()
        assert 'text_language' not in info
        assert 'quote_language' not in info
        # both set - should be included by name
        lang1 = Language.objects.first()
        lang2 = Language.objects.last()
        note.text_language = lang1
        note.quote_language = lang2
        info = note.info()
        assert info['text_language'] == lang1.name
        assert info['quote_language'] == lang2.name

        # text translation
        # - not set, not included
        info = note.info()
        assert 'text_translation' not in info
        # - included when set
        note.text_translation = 'some translated text goes here'
        info = note.info()
        assert info['text_translation'] == note.text_translation

        # author
        # - not set, not included
        info = note.info()
        assert 'author' not in info
        # - included when set
        note.author = Person.objects.create(authorized_name='Derrida, Jacques')
        info = note.info()
        assert info['author'] == 'Derrida, Jacques'

    def test_iiif_image_selection(self):
        annotation = Intervention()
        # no canvas or image selection
        assert not annotation.iiif_image_selection()

        annotation.canvas = Canvas()
        # canvas set but no image region
        assert not annotation.iiif_image_selection()

        # both canvas and image region set
        annotation.extra_data['image_selection'] = {
            'x': "21.58%",
            'y': "49.40%",
            'h': "13.50%",
            'w': "24.68%"
        }
        img = annotation.iiif_image_selection()
        # should return a piffle iiif image object
        assert img
        iiif_region_info = img.region.as_dict()
        assert iiif_region_info['percent']
        assert iiif_region_info['x'] == 21.58
        assert iiif_region_info['y'] == 49.4
        assert iiif_region_info['width'] == 24.68
        assert iiif_region_info['height'] == 13.5

    def test_admin_thumbnail(self):
        annotation = Intervention()
        # no canvas or image selection
        assert not annotation.admin_thumbnail()

        annotation.canvas = Canvas()
        # canvas set but no image region
        assert annotation.admin_thumbnail() == \
            '<img src="%s" />' % annotation.canvas.image.mini_thumbnail()

        # both canvas and image region set
        annotation.extra_data['image_selection'] = {
            'x': "21.58%",
            'y': "49.40%",
            'h': "13.50%",
            'w': "24.68%"
        }
        assert annotation.admin_thumbnail() == \
            '<img src="%s" />' % annotation.iiif_image_selection().mini_thumbnail()

    def test_is_verbal(self):

        note = Intervention()
        assert not note.is_verbal()
        note.text = 'foobar'
        assert note.is_verbal()

    def test_annotation_type(self):
        note = Intervention.objects.create()
        # no tags, no text - nonverbal annotation
        assert note.annotation_type == ['nonverbal annotation']

        note.text = 'some content'
        assert note.annotation_type == ['verbal annotation']

        note.tags.set([
            Tag.objects.get(name='underlining'),
            Tag.objects.get(name='marginal mark'),
            Tag.objects.get(name='blue ink'),
            Tag.objects.get(name='transcription uncertain'),
        ])
        assert set(note.annotation_type) == \
            set(['underlining', 'marginal mark', 'verbal annotation'])
        note.text = ''
        note.tags.set([
            Tag.objects.get(name='line'),
            Tag.objects.get(name='black ink'),
            Tag.objects.get(name='text illegible'),
        ])
        assert set(note.annotation_type) == \
            set(['line', 'nonverbal annotation'])

    def test_inke(self):
        note = Intervention.objects.create()
        # no tags
        assert note.ink == []

        note.tags.set([
            Tag.objects.get(name='underlining'),
            Tag.objects.get(name='marginal mark'),
            Tag.objects.get(name='blue ink'),
            Tag.objects.get(name='transcription uncertain'),
        ])
        assert note.ink == ['blue ink']

        note.tags.set([
            Tag.objects.get(name='line'),
            Tag.objects.create(name='pencil'),
            Tag.objects.get(name='black ink')
        ])
        assert set(note.ink) == set(['black ink', 'pencil'])


class TestInterventionQuerySet(TestCase):

    def test_sorted_by_page_loc(self):

        # create three note objects
        note1 = Intervention.objects.create()
        note2 = Intervention.objects.create()
        note3 = Intervention.objects.create()
        # snippet reused from above
        extra_data = {}
        extra_data['image_selection'] = {
            'x': "21.58%",
            'y': "49.40%",
            'h': "13.50%",
            'w': "24.68%"
        }
        # save each with a different y value for their page location
        note1.extra_data = extra_data
        note1.save()
        extra_data['image_selection']['y'] = '23.00%'
        note2.extra_data = extra_data
        note2.save()
        extra_data['image_selection']['y'] = '91.00%'
        note3.extra_data = extra_data
        note3.save()
        # method should return a list of annotations sorted by y value
        sorted_notes = Intervention.objects.all().sorted_by_page_loc()
        assert sorted_notes == [note2, note1, note3]


class TestInterventionViews(TestCase):

    def setUp(self):
        # create an admin user to test autocomplete views
        self.password = 'pass!@#$'
        self.admin = get_user_model().objects.create_superuser('testadmin',
            'test@example.com', self.password)

        # create staff user to test logged in but no perms
        self.staffer = get_user_model().objects.create_user('tester',
            'tester@example.com', self.password, is_staff=True)


    def test_tag_autocomplete(self):
        tag_autocomplete_url = reverse('interventions:tag-autocomplete')
        result = self.client.get(tag_autocomplete_url,
            params={'q': 'circ'})
        # not allowed to anonymous user
        assert result.status_code == 302

        # login as an admin user
        self.client.login(username=self.admin.username, password=self.password)

        result = self.client.get(tag_autocomplete_url, {'q': 'circ'})
        assert result.status_code == 200
        # decode response to inspect
        data = json.loads(result.content.decode('utf-8'))
        assert data['results'][0]['text'] == 'circling'

        # filter by mode
        tag_autocomplete_url = reverse('interventions:tag-autocomplete',
            kwargs={'mode': 'annotation'})
        result = self.client.get(tag_autocomplete_url, {'q': 'line'})
        assert result.status_code == 200
        # decode response to inspect
        data = json.loads(result.content.decode('utf-8'))
        assert data['results'][0]['text'] == 'line'

        tag_autocomplete_url = reverse('interventions:tag-autocomplete',
            kwargs={'mode': 'insertion'})
        result = self.client.get(tag_autocomplete_url, {'q': 'line'})
        assert result.status_code == 200
        # decode response to inspect
        data = json.loads(result.content.decode('utf-8'))
        assert not data['results']

    def test_iiif_permissions(self):
        # iiif views of digitized content are restricted to users
        # with appropriate permissions due to copyright concerns

        manifest = Manifest.objects.create(short_id='foo')
        canvas = Canvas.objects.create(short_id='bar', manifest=manifest,
            order=0)

        iiif_urls = [
            reverse('djiffy:list'),
            reverse('djiffy:manifest', kwargs={'id': manifest.short_id}),
            reverse('djiffy:canvas',
                kwargs={'manifest_id': manifest.short_id,
                        'id': canvas.short_id}),
            reverse('djiffy:canvas-autocomplete'),
        ]

        # without logging in, should get redirect to login page
        for url in iiif_urls:
            response = self.client.get(url)
            assert response.status_code == 302
            assert response.url == '%s?next=%s' % (settings.LOGIN_URL, url)

        # logged in but insufficient privileges - 403 permission denied
        self.client.login(username=self.staffer.username, password=self.password)
        for url in iiif_urls:
            assert self.client.get(url).status_code == 403

        # logged in as admin - should be able to access the content
        self.client.login(username=self.admin.username, password=self.password)
        for url in iiif_urls:
            assert self.client.get(url).status_code == 200

    def test_canvas_detail(self):
        # login as an staff user without permission to view canvas
        # but not add annotations
        self.staffer.user_permissions.add(Permission.objects.get(codename='view_canvas'))

        self.client.login(username=self.staffer.username, password=self.password)

        # canvas detail logic is tested in djiffy,
        # but test local customization to catch any
        # breaks in the template rendering

        manifest = Manifest.objects.create(short_id='foo')
        canvas = Canvas.objects.create(short_id='bar', manifest=manifest,
            order=0)

        canvas_url = reverse('djiffy:canvas',
            kwargs={'manifest_id': canvas.manifest.short_id, 'id': canvas.short_id})
        response = self.client.get(canvas_url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'djiffy/canvas_detail.html')
        self.assertTemplateNotUsed(response, 'books/canvas_detail.html')
        self.assertNotContains(response, 'annotator.min.js',
            msg_prefix='Annotator not enabled for user without annotation add permission')

        # login as an admin user
        self.client.login(username=self.admin.username, password=self.password)
        response = self.client.get(canvas_url)

        # check that languages are passed in to template via context
        assert 'languages_js' in response.context

        # check that derrida name is set in context
        assert 'default_intervener' in response.context

        self.assertContains(response, 'css/derrida-annotator.css',
            msg_prefix='canvas detail page includes local annotator styles')
        self.assertContains(response, 'interventions-plugin.js',
            msg_prefix='canvas detail page includes local intervention plugin')

        # check that expected autocomplete urls are present
        # NOTE: these tests fail if compression is enabled, because the
        # expected urls are in a javascript block
        # NOTE: currently tag autocomplete is annotation tags only
        self.assertContains(response,
            reverse('interventions:tag-autocomplete', kwargs={'mode': 'annotation'}),
            msg_prefix='annotator init includes tag autocomplete url')
        # username configured
        self.assertContains(response,
            'app.ident.identity = "%s";' % self.admin.username,
            msg_prefix='Logged in user username passed to annotator')
        self.assertContains(response,
            reverse('books:language-autocomplete'),
            msg_prefix='annotator init includes language autocomplete url')


#: override_settings and use test haystack connection
@override_settings(HAYSTACK_CONNECTIONS=settings.HAYSTACK_TEST_CONNECTIONS)
class TestInterventionSolrViews(TestCase):
    fixtures = ['test_interventions.json']

    @pytest.mark.haystack
    def test_intervention_list(self):
        intervention_list_url = reverse('interventions:list')
        response = self.client.get(intervention_list_url)
        assert response.status_code == 200
        assert 'object_list' in response.context
        assert isinstance(response.context['object_list'][0], SearchResult)
        assert len(response.context['object_list']) == \
            Intervention.objects.count()
        self.assertContains(response, '%d Results' % Intervention.objects.count(),
            msg_prefix='total number of results displayed')

        # default order - author of annotated work
        first_result = response.context['object_list'][0]
        alpha_author = Intervention.objects \
            .order_by('canvas__manifest__instance__work__authors__authorized_name',
                'canvas__label') \
            .first()
        assert first_result.pk == str(alpha_author.pk)
        # check details included in template
        # annotation type
        for annotype in first_result.annotation_type:
            self.assertContains(response, annotype)
        # canvas image & link
        self.assertContains(response,
            reverse('books:canvas-detail', args=[first_result.item_slug, first_result.canvas_id]),
            msg_prefix='annotation should link to canvas detail')
        self.assertContains(response,
            reverse('books:canvas-image', args=[first_result.item_slug, first_result.canvas_id, 'smthumb']),
            msg_prefix='annotation should display local thumbnail image')
        self.assertContains(response,
            reverse('books:canvas-image', args=[first_result.item_slug, first_result.canvas_id, 'smthumb', '@2x']),
            msg_prefix='annotation should display include 2x thumbnail image')
        self.assertContains(response,
            reverse('books:detail', args=[first_result.item_slug]),
            msg_prefix='should link to annotated book')
        self.assertContains(response, first_result.item_title,
            msg_prefix='should display annotated book title')
        # first result item has no print year
        self.assertContains(response, first_result.annotated_page,
            msg_prefix='should display label of annotated page')

        # keyword search
        response = self.client.get(intervention_list_url, {'query': 'kritisieren'})
        assert response.status_code == 200
        assert len(response.context['object_list']) == 1

        # filter by annotated work author
        response = self.client.get(intervention_list_url, {'hand': ['Jacques Derrida']})
        assert len(response.context['object_list']) == 1

        # filter by ink
        response = self.client.get(intervention_list_url, {'ink': ['blue ink']})
        assert len(response.context['object_list']) == 1

        # range filter
        # - work year
        response = self.client.get(intervention_list_url,
                                   {'item_work_year_0': 1950})
        # use total as a proxy of count() and to avoid pagination issues
        assert response.context['total'] == \
            Intervention.objects.filter(
                canvas__manifest__instance__work__year__gte=1950
            ).count()
        response = self.client.get(intervention_list_url,
            {'item_work_year_0': 1927, 'item_work_year_1': 1950})
        assert response.context['total'] == \
            Intervention.objects.filter(
                canvas__manifest__instance__work__year__lte=1950,
                canvas__manifest__instance__work__year__gte=1927
            ).count()
        # - copyright year
        response = self.client.get(intervention_list_url,
                                   {'item_copyright_year_0': 1950})
        # use total as a proxy of count() and to avoid pagination issues
        assert response.context['total'] == \
            Intervention.objects.filter(
                canvas__manifest__instance__copyright_year__gte=1950
            ).count()
        response = self.client.get(intervention_list_url,
            {'item_copyright_year_0': 1927,
             'item_copyright_year_1': 1950})
        assert response.context['total'] == \
            Intervention.objects.filter(
                canvas__manifest__instance__copyright_year__lte=1950,
                canvas__manifest__instance__copyright_year__gte=1927
            ).count()
        # - print year
        response = self.client.get(intervention_list_url,
                                   {'item_print_year_0': 1950})
        # use total as a proxy of count() and to avoid pagination issues
        # pass date as ISO string since these are date fields but we're
        # only checking very coarsely by year, don't need to check date known
        # flags
        assert response.context['total'] == \
            Intervention.objects.filter(
                canvas__manifest__instance__print_date__gte='1950-01-01'
            ).count()
        response = self.client.get(
            intervention_list_url,
            {'item_print_year_0': 1927, 'item_print_year_1': 1950}
        )
        assert response.context['total'] == \
            Intervention.objects.filter(
                canvas__manifest__instance__print_date__lte='1950-12-31',
                canvas__manifest__instance__print_date__gte='1927-01-01'
            ).count()
        # The aggregate values should be in the cache with values as expected
        # - This reuses the code from the view, which is ugly, but
        # it avoids problems with a changed fixture that would be
        # caused by hardcoding it
        aggregate_queries = {
            'item_work_year_max': Max('canvas__manifest__instance__work__year'),
            'item_work_year_min': Min('canvas__manifest__instance__work__year'),
            'item_copyright_year_max': Max('canvas__manifest__instance__copyright_year'),
            'item_copyright_year_min': Min('canvas__manifest__instance__copyright_year'),
            'item_print_year_max': Max('canvas__manifest__instance__print_date'),
            'item_print_year_min': Min('canvas__manifest__instance__print_date'),
        }
        ranges = (
            Intervention.objects
            .filter(canvas__manifest__instance__is_extant=True)
            .aggregate(**aggregate_queries)
        )
        # pre-process datetime.date instances to get just
        # year as an integer
        for field, value in ranges.items():
            if isinstance(value, datetime.date):
                ranges[field] = value.year
        assert ranges == cache.get('intervention_ranges', None)


class TestExtendedCanvasAutocomplete(TestCase):

    fixtures = ['sample_work_data.json']

    def setUp(self):
        self.manif1 = Manifest.objects.create(short_id='bk123', label='Foobar')
        self.pages = Canvas.objects.bulk_create([
            Canvas(label='P1', short_id='pg1', order=0, manifest=self.manif1),
            Canvas(label='P2', short_id='pg2', order=1, manifest=self.manif1),
            Canvas(label='P3', short_id='pg3', order=2, manifest=self.manif1)
        ])
        self.manif2 = Manifest.objects.create(short_id='bk456', label='Book 2')
        self.instance = Instance.objects.get(work__short_title__contains="La vie")

        # create an admin user to test autocomplete views
        self.password = 'pass!@#$'
        self.admin = get_user_model().objects.create_superuser('testadmin',
            'test@example.com', self.password)

    def test_canvas_autocomplete(self):
        canvas_autocomplete_url = reverse('djiffy:canvas-autocomplete')
        # normal functionality NOT broken
        self.client.login(username=self.admin.username, password=self.password)
        response = self.client.get(canvas_autocomplete_url, {'q': 'p1'})
        assert response.status_code == 200
        data = json.loads(response.content.decode('utf-8'))
        assert 'results' in data
        assert data['results'][0]['text'] == str(self.pages[0])
        # add a book instance pk to the result
        # avoid params so as to simulate the get string that
        # dal expects
        response = self.client.get(
            canvas_autocomplete_url,
            {'q': 'p1', 'forward': ('{"instance": "%s"}' % self.instance.pk)}
        )
        assert response.status_code == 200

        data = json.loads(response.content.decode('utf-8'))
        # key exists
        assert 'results' in data
        # but it is empty because no instance is associated
        assert not data['results']
        # now try with an association set
        self.instance.digital_edition = self.manif1
        self.instance.save()
        response = self.client.get(
            canvas_autocomplete_url,
            {'q': 'p1', 'forward': '{"instance": "%s"}' % self.instance.pk}
        )
        data = json.loads(response.content.decode('utf-8'))
        assert 'results' in data
        assert data['results'][0]['text'] == str(self.pages[0])

        # test forwarding manifest id
        response = self.client.get(
            canvas_autocomplete_url,
            {'q': 'p1', 'forward': '{"manifest": "%s"}' % self.manif1.pk}
        )
        data = json.loads(response.content.decode('utf-8'))
        assert 'results' in data
        assert data['results'][0]['text'] == str(self.pages[0])


class TestInterventionAutocomplete(TestCase):

    fixtures = ['sample_work_data.json']

    def setUp(self):
        self.manif = Manifest.objects.create(short_id='bk123', label='Foobar')
        self.manif2 = Manifest.objects.create(short_id='bk456', label='Baz')
        self.canvas = Canvas.objects.create(
            label='P1',
            short_id='pg1',
            order=0,
            manifest=self.manif,
            uri='http://so.me/iiif/id')
        self.canvas2 = Canvas.objects.create(
            label='P2',
            short_id='pg2',
            order=1,
            manifest=self.manif2,
            uri='http://so.me/iiif/id2',
        )
        self.instance = Instance.objects.get(work__short_title__contains="La vie")
        self.instance.digital_edition = self.manif2
        self.instance.save()
        # create an admin user to test autocomplete views
        self.password = 'pass!@#$'
        self.admin = get_user_model().objects.create_superuser('testadmin',
            'test@example.com', self.password)

        self.note1 = Intervention.objects.create(uri=self.canvas.uri, canvas=self.canvas)
        self.note2 = Intervention.objects.create(uri=self.canvas.uri, canvas=self.canvas)
        self.note3 = Intervention.objects.create(uri=self.canvas2.uri, canvas=self.canvas2)

    def test_intervention_autocomplete(self):

        note1 = self.note1
        note2 = self.note2
        intervention_autocomplete_url = reverse('interventions:autocomplete')

        # not logged in client can't have permissions
        response = self.client.get(intervention_autocomplete_url)
        assert response.status_code == 302

        # logged in client has permission as superuser
        self.client.login(username=self.admin.username, password=self.password)
        response = self.client.get(intervention_autocomplete_url)
        data = json.loads(response.content.decode('utf-8'))
        assert response.status_code == 200
        assert 'results' in data
        # both notes should be returned
        assert len(data['results']) == 3

        # filterable notes, testing the text field lookups
        note1.quote = 'test'
        note2.quote = 'foo2'
        note2.text_language = Language.objects.get(name='French')
        note1.save()
        note2.save()
        # 'test' should return note1 but not note2
        response = self.client.get(intervention_autocomplete_url, {'q': 'test'})
        data = json.loads(response.content.decode('utf-8'))
        assert 'results' in data
        assert len(data['results']) == 1
        assert data['results'][0]['text'] == 'test (P1)'

        # testing fk lookups: 'French' should return note2 but not note 1
        response = self.client.get(intervention_autocomplete_url, {'q': 'French'})
        data = json.loads(response.content.decode('utf-8'))
        assert 'results' in data
        assert len(data['results']) == 1
        assert str(data['results'][0]['text']) == 'foo2 (P1)'

        # Test tag handling since it's a more complicated query
        note1.quote = 'test2'
        note1.save()
        tags = Tag.objects.filter(name__in=['underlining', 'arrow'])
        note1.tags.set(tags)
        response = self.client.get(intervention_autocomplete_url, {'q': 'underlining'})
        data = json.loads(response.content.decode('utf-8'))
        assert 'results' in data
        assert len(data['results']) == 1
        assert data['results'][0]['text'] == ('test2 (P1)')

        # Test instance handling - note3 is associated with the instance
        note3 = self.note3
        note3.quote = 'test3'
        note3.save()
        response = self.client.get(intervention_autocomplete_url,
            {'forward': ('{"instance": "%s"}' % self.instance.pk)})
        data = json.loads(response.content.decode('utf-8'))
        assert response.status_code == 200
        assert 'results' in data
        # only note 3 should be returned
        assert len(data['results']) == 1
        assert data['results'][0]['text'] == ('test3 (P2)')


class TestGetDefaultIntervener(TestCase):

    def setUp(self):
        self.derrida = Person.objects.create(
                       authorized_name='Derrida, Jacques')

    def test_get_default_intervener(self):

        # if Derrida exists, the function retrieves his Person object
        derrida = get_default_intervener()
        assert derrida
        assert derrida == self.derrida.pk

        # if he does not, it returns None to use as a default on the model
        self.derrida.delete()
        derrida = get_default_intervener()
        assert not derrida
