from django.test import TestCase

from .models import Tag, TYPES


class TestTag(TestCase):

    #  test custom queryset filters based on initial set of preloaded tags

    def test_qs_for_annotations(self):
        # create insertion-only tag for testing
        Tag.objects.create(name='post-it note', applies_to=TYPES.INSERTION)

        annotation_tags = Tag.objects.for_annotations()
        # annotation only tag
        assert annotation_tags.filter(name='underlining').exists()
        # annotation/insertion tag
        assert annotation_tags.filter(name='transcription uncertain').exists()
        # insertion only
        assert not annotation_tags.filter(name='post-it note').exists()

    def test_qs_for_insertions(self):
        # create insertion-only tag for testing
        Tag.objects.create(name='post-it note', applies_to=TYPES.INSERTION)

        insertion_tags = Tag.objects.for_insertions()
        # annotation only tag
        assert not insertion_tags.filter(name='underlining').exists()
        # annotation/insertion tag
        assert insertion_tags.filter(name='transcription uncertain').exists()
        # insertion only
        assert insertion_tags.filter(name='post-it note').exists()
