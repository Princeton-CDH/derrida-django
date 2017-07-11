from attrdict import AttrDict
from annotator_store.models import BaseAnnotation
from django.db import models
from djiffy.models import Canvas

from derrida.common.models import Named, Notable
from derrida.books.models import Language
# from derrida.people.models import Person


#: intervention type codes to distinguish annotations and insertions
INTERVENTION_TYPES = AttrDict({
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
        return self.filter(applies_to__contains=INTERVENTION_TYPES.ANNOTATION)

    def for_insertions(self):
        '''Find tags that apply to insertions'''
        return self.filter(applies_to__contains=INTERVENTION_TYPES.INSERTION)


class Tag(Named, Notable):
    APPLIES_TO_CHOICES = (
        (INTERVENTION_TYPES.ANNOTATION, 'Annotations only'),
        (INTERVENTION_TYPES.INSERTION, 'Insertions only'),
        (INTERVENTION_TYPES.BOTH, 'Both Annotations and Insertions'),
    )
    applies_to = models.CharField(max_length=2, choices=APPLIES_TO_CHOICES,
        default=INTERVENTION_TYPES.BOTH,
        help_text='Type or types of interventions this tag is applicable to.')

    objects = TagQuerySet.as_manager()


class Intervention(BaseAnnotation):

    INTERVENTION_TYPE_CHOICES = (
        (INTERVENTION_TYPES.ANNOTATION, 'Annotation'),
        (INTERVENTION_TYPES.INSERTION, 'Insertion'),
    )
    intervention_type = models.CharField(
        max_length=2,
        choices=INTERVENTION_TYPE_CHOICES,
        default=INTERVENTION_TYPES.ANNOTATION,
    )

    #: associated IIIF :class:`djiffy.models.Canvas` for interventions
    #: related to an image
    canvas = models.ForeignKey(Canvas, null=True, blank=True)
    #: Tags to describe the intervention and its characteristics;
    #: many-to-many relationship to :class:`Tag`
    tags = models.ManyToManyField(Tag, blank=True,
        help_text='Tags to describe this intervation and its characteristics')
    #: language of the intervention text (i.e. :attr:`text`)
    text_language = models.ForeignKey(Language, null=True, blank=True,
        help_text='Language of the intervention text', related_name='+')
    #: translation language of the intervention text (i.e. :attr:`text`)
    text_translation = models.TextField(blank=True,
        help_text='Translation of the intervention text (optional)')

    #: language of the quoted text or anchor text (i.e. :attr:`quote`)
    quote_language = models.ForeignKey(Language, null=True, blank=True,
            help_text='Language of the anchor text', related_name='+')

    # todo
    # author = models.ForeignKey(Person, null=True, blank=True)

    class Meta:
        # extend default permissions to add a view option
        # change_annotation and delete_annotation provided by django
        permissions = (
            ('view_intervention', 'View intervention'),
        )

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

        # If the object does not yet exist in the database, it must be
        # saved before adding foreign key or many-to-many relationships.
        if self._state.adding:
            super(Intervention, self).save()

        # Set any tags that are passed if they already exist in the db
        # (tag vocabulary is enforced; unrecognized tags are ignored)
        if 'tags' in data:
            tags = Tag.objects.filter(name__in=data['tags'])
            self.tags.set(tags)
            del data['tags']

        # annotation text language; unset or invalid clears out the language
        try:
            self.text_language = Language.objects.get(name=data.get('text_language', None))
        except Language.DoesNotExist:
            self.text_language = None

        # quote/anchor text language; unset or invalid clears it out
        try:
            self.quote_language = Language.objects.get(name=data.get('quote_language', None))
        except Language.DoesNotExist:
            self.quote_language = None

        self.text_translation = data.get('text_translation', '')

        # remove fields if present, but don't error if they are not
        for field in ['text_language', 'quote_language', 'text_translation']:
            try:
                del data[field]
            except KeyError:
                pass

        return data

    def info(self):
        '''Return a dictionary of fields and values for
        display in the JSON object representation of the annotation.'''

        # Must include all local database fields in the output
        info = super(Intervention, self).info()
        info.update({
            'tags': [tag.name for tag in self.tags.all()],
        })
        # languages - display language name
        if self.text_language:
            info['text_language'] = self.text_language.name
        if self.quote_language:
            info['quote_language'] = self.quote_language.name
        if self.text_translation:
            info['text_translation'] = self.text_translation

        return info
