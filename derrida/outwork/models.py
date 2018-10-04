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

    def __repr__(self):
        '''object representation; use slug as identifier'''
        return '<Outwork: %s>' % self.slug

    def get_slug(self):
        '''customize slug logic to include year and ensure url is
        under outwork/'''
        slug = super(Outwork, self).get_slug()
        # if added as a child of the outwork list page,
        # mezzanine adds an outwork prefix we don't want; remove it
        # before customizing the url
        if slug.startswith('outwork/'):
            slug = slug[len('outwork/'):]

        if self.publish_date:
            year = self.publish_date.year
        else:
            year = self.created.year
        # remove the extra '/outwork/' if a child of the outwork page
        return '/'.join(['outwork', str(year), slug])

    def is_published(self):
        '''Return whether the :class:`Outwork` is published.'''
        return self.status == CONTENT_STATUS_PUBLISHED
