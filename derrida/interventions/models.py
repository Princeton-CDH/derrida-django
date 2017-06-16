from annotator_store.models import BaseAnnotation
from django.db import models
from djiffy.models import Canvas

# from derrida.people.models import Person


class Intervention(BaseAnnotation):

    ANNOTATION = 'A'
    INSERTION = 'I'
    INTERVENTION_TYPE_CHOICES = (
        (ANNOTATION, 'Annotation'),
        (INSERTION, 'Insertion'),
    )
    intervention_type = models.CharField(
        max_length=2,
        choices=INTERVENTION_TYPE_CHOICES,
        default=ANNOTATION,
    )

    #: associated IIIF :cjass:`djiffy.models.Canvas` for interventions
    #: related to an image
    canvas = models.ForeignKey(Canvas, null=True, blank=True)
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
        return self.intervention_type == self.ANNOTATION

    def is_insertion(self):
        return self.intervention_type == self.INSERTION

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