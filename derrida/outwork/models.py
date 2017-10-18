from django.db import models
from mezzanine.core.models import RichText, CONTENT_STATUS_PUBLISHED
from mezzanine.core.managers import DisplayableManager
from mezzanine.pages.models import Page

from derrida.people.models import Person


class Outwork(Page, RichText):
    author = models.ForeignKey(Person, blank=True, null=True,
        help_text='Author of the content, if known (optional)')
    orig_pubdate = models.DateField("Original Publication Date",
        blank=True, null=True,
        help_text='''Original publication date for content published elsewhere,
        if known''')

    # use displayable manager for access to published queryset filter, etc.
    objects = DisplayableManager()

    def get_slug(self):
        slug = super(Outwork, self).get_slug()
        if self.publish_date:
            year = self.publish_date.year
        else:
            year = self.created.year
        return '/'.join(['outwork', str(year), slug])

    def is_published(self):
        return self.status == CONTENT_STATUS_PUBLISHED
