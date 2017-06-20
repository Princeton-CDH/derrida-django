from unittest.mock import Mock, patch

from django.test import TestCase
from djiffy.models import Canvas, Manifest

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

    def test_info(self):
        note = Intervention.objects.create()

        # tags should be an empty list when none are set
        assert not note.info()['tags']
        tags = ['circling', 'arrow']
        note.handle_extra_data({'tags': tags}, Mock())
        # order not guaranteed / not important; compare as a set
        assert set(note.info()['tags']) == set(tags)

    def test_iiif_image_selection(self):
        # borrowed from winthrop code

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
        # borrowed from winthrop code

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


