import json
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from djiffy.models import Canvas, Manifest

from derrida.books.models import Language
from .models import Tag, INTERVENTION_TYPES, Intervention


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

        ### languages ##

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


class TestInterventionViews(TestCase):

    def setUp(self):
        # create an admin user to test autocomplete views
        self.password = 'pass!@#$'
        self.admin = get_user_model().objects.create_superuser('testadmin',
            'test@example.com', self.password)

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

    def test_canvas_detail(self):
        # canvas detail logic is tested in djiffy,
        # but test local customization to catch any
        # breaks in the template rendering

        manifest = Manifest.objects.create(short_id='foo')
        canvas = Canvas.objects.create(short_id='bar', manifest=manifest,
            order=0)

        canvas_url = reverse('djiffy:canvas',
            kwargs={'manifest_id': canvas.manifest.short_id, 'id': canvas.short_id})
        response = self.client.get(canvas_url)
        self.assertTemplateUsed(response, 'djiffy/canvas_detail.html')
        self.assertNotContains(response, 'annotator.min.js',
            msg_prefix='Annotator not enabled for user without annotation add permission')

        # login as an admin user
        self.client.login(username=self.admin.username, password=self.password)
        response = self.client.get(canvas_url)
        self.assertContains(response, 'css/derrida-annotator.css',
            msg_prefix='canvas detail page includes local annotator styles')
        self.assertContains(response, 'interventions-plugin.js',
            msg_prefix='canvas detail page includes local intervention plugin')
        # check that expected autocomplete urls are present
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



