from attrdict import AttrDict
from annotator_store.models import BaseAnnotation
from django.db import models
from djiffy.models import Canvas

from derrida.common.models import Named, Notable
# from derrida.people.models import Person


#: intervention type codes to distinguish annotations and insertions
TYPES = AttrDict({
    'ANNOTATION': 'A',
    'INSERTION': 'I',
    'BOTH': 'AI',
})


class TagQuerySet(models.QuerySet):
    '''Custom :class:`~django.db.models.QuerySet` for :class`Tag` to
    make it easy to find tags that apply to a particular kind of
    Intervention.'''

    def for_annotations(self):
        '''Find tags that apply to annotations'''
        return self.filter(applies_to__contains=TYPES.ANNOTATION)

    def for_insertions(self):
        '''Find tags that apply to insertions'''
        return self.filter(applies_to__contains=TYPES.INSERTION)


class Tag(Named, Notable):
    APPLIES_TO_CHOICES = (
        (TYPES.ANNOTATION, 'Annotations only'),
        (TYPES.INSERTION, 'Insertions only'),
        (TYPES.BOTH, 'Both Annotations and Insertions'),
    )
    applies_to = models.CharField(max_length=2, choices=APPLIES_TO_CHOICES,
        default=TYPES.BOTH,
        help_text='Type or types of interventions this tag is applicable to.')

    objects = TagQuerySet.as_manager()


class Intervention(BaseAnnotation):

    INTERVENTION_TYPE_CHOICES = (
        (TYPES.ANNOTATION, 'Annotation'),
        (TYPES.INSERTION, 'Insertion'),
    )
    intervention_type = models.CharField(
        max_length=2,
        choices=INTERVENTION_TYPE_CHOICES,
        default=TYPES.ANNOTATION,
    )

    #: associated IIIF :cjass:`djiffy.models.Canvas` for interventions
    #: related to an image
    canvas = models.ForeignKey(Canvas, null=True, blank=True)
    #: Tags to describe the intervention and its characteristics
    tags = models.ManyToManyField(Tag, blank=True)

    # todo
    # author = models.ForeignKey(Person, null=True, blank=True)

    def save(self, *args, **kwargs):
        # for image annotation, URI should be set to canvas URI; look up
        # canvas by URI and associate with the record

        # if canvas is already set and uri matches annotation uri, do nothing
        if self.canvas and self.uri == self.canvas.uri:
            pass
        else:
            # otherwise, lookup canvas and associate
            # (clear out in case there is no match for the new uri)
            self.canvas = None
            try:
                self.canvas = Canvas.objects.get(uri=self.uri)
            except Canvas.DoesNotExist:
                pass
        super(Intervention, self).save()

    def is_annotation(self):
        return self.intervention_type == TYPES.ANNOTATION

    def is_insertion(self):
        return self.intervention_type == TYPES.INSERTION

    # NOTE: iiif_image_selection and admin_thumbnail borrowed
    # directly from cdh winthrop annotation code

    img_info_to_iiif = {'w': 'width', 'h': 'height', 'x': 'x', 'y': 'y'}

    def iiif_image_selection(self):
        # if image selection information is present in annotation
        # and canvas is associated, generated a IIIF image for the
        # selected portion of the canvas
        if 'image_selection' in self.extra_data and self.canvas:
            # convert stored image info into the format used by
            # piffle for generating iiif image region
            img_selection = {
                self.img_info_to_iiif[key]: float(val.rstrip('%'))
                for key, val in self.extra_data['image_selection'].items()
                if key in self.img_info_to_iiif
            }
            return self.canvas.image.region(percent=True, **img_selection)

    def admin_thumbnail(self):
        img_selection = self.iiif_image_selection()
        # if image selection is available, display small thumbnail
        if img_selection:
            return u'<img src="%s" />' % img_selection.mini_thumbnail()
        # otherwise, if canvas is set, display canvas small thumbnail
        elif self.canvas:
            return u'<img src="%s" />' % self.canvas.image.mini_thumbnail()
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True

    def handle_extra_data(self, data, request):
        '''Handle "extra" data that is not part of the stock annotation
        data model.  Used to support custom fields that are
        specific to :class:`Intervention`.  Data is as provided from json
        request data, as sent by annotator.js.'''

        # Catch any SQL Foreign Key issues by saving before processing the
        # extra data using super()
        # FIXME: only necessary if no pk is set?
        # super(Intervention, self).save()

        # set any tags that are passed if they already exist in the db
        # (tag vocabulary is enforced; unrecognized tags are ignored)
        if 'tags' in data:
            tags = Tag.objects.filter(name__in=data['tags'])
            self.tags.set(tags)
            del data['tags']

        return data

    def info(self):
        '''Return a dictionary of fields and values for
        display in the JSON object representation of the annotation.'''

        # Must include all local database fields in the output
        info = super(Intervention, self).info()
        info.update({
            'tags': [tag.name for tag in self.tags.all()],
        })
        return info
