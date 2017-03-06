from django.test import TestCase
from django.contrib.contenttypes.models import ContentType


from .models import SourceType, Bibliography, Footnote


class TestSourceType(TestCase):
    # Add a testing fixture until project team decides on a set vocabulary
    # to load in a migration
    fixtures = ['initial_sourcetypes.json']
    def test_item_count(self):
        src_type = SourceType.objects.first()
        assert src_type.item_count() == 0

        bibl = Bibliography.objects.create(bibliographic_note='citation',
            source_type=src_type)
        assert src_type.item_count() == 1


class TestBibliography(TestCase):
    # Add a testing fixture until project team decides on a set vocabulary
    # to load in a migration
    fixtures = ['initial_sourcetypes.json']
    def test_str(self):
        src_type = SourceType.objects.first()
        bibl = Bibliography.objects.create(bibliographic_note='citation',
            source_type=src_type)
        assert str(bibl) == 'citation'

    def test_footnote_count(self):
        src_type = SourceType.objects.first()
        bibl = Bibliography.objects.create(bibliographic_note='citation',
            source_type=src_type)
        assert bibl.footnote_count() == 0

        # find an arbitrary content type to attach a footnote to
        content_type = ContentType.objects.first()
        Footnote.objects.create(bibliography=bibl, content_type=content_type,
            object_id=1, is_agree=False)
        assert bibl.footnote_count() == 1
