import json
import re
import string

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from djiffy.models import Canvas, Manifest
from sortedm2m.fields import SortedManyToManyField
from unidecode import unidecode

from derrida.common.models import Named, Notable, DateRange
from derrida.places.models import Place
from derrida.people.models import Person
from derrida.footnotes.models import Footnote

Q = models.Q


# TODO: could work/instance count be refactored for more general use?

class WorkCount(models.Model):
    '''Mix-in for models related to works; adds work count property and link to
    associated works'''
    class Meta:
        abstract = True

    def work_count(self):
        base_url = reverse('admin:books_work_changelist')
        return mark_safe('<a href="%s?%ss__id__exact=%s">%s</a>' % (
                            base_url,
                            self.__class__.__name__.lower(),
                            self.pk,
                            self.work_set.count()
                ))
    work_count.short_description = '# works'
    # NOTE: possible to use a count field for admin ordering!
    # see https://mounirmesselmeni.github.io/2016/03/21/how-to-order-a-calculated-count-field-in-djangos-admin/
    # book_count.admin_order_field = 'work__count'


class InstanceCount(models.Model):
    '''Mix-in for models related to books; adds book count property and link to
    associated books'''
    class Meta:
        abstract = True

    def instance_count(self):
        base_url = reverse('admin:books_instance_changelist')
        return mark_safe('<a href="%s?%ss__id__exact=%s">%s</a>' % (
                            base_url,
                            self.__class__.__name__.lower(),
                            self.pk,
                            self.instance_set.count()
                ))
    instance_count.short_description = '# instances'


class Subject(Named, Notable, WorkCount):
    '''Subject categorization for books'''
    #: optional uri
    uri = models.URLField(blank=True, null=True)


class Language(Named, Notable, WorkCount, InstanceCount):
    '''Language that a book is written in or a language included in a book'''
    #: optional uri
    uri = models.URLField(blank=True, null=True)


class Publisher(Named, Notable, InstanceCount):
    '''Publisher of a book'''
    pass


class OwningInstitution(Named, Notable, InstanceCount):
    '''Institution that owns the extant copy of a book'''
    #: short name (optioal)
    short_name = models.CharField(max_length=255, blank=True,
        help_text='Optional short name for admin display')
    #: contact information
    contact_info = models.TextField()
    #: :class:`~derrida.places.models.Place`
    place = models.ForeignKey(Place)

    def __str__(self):
        return self.short_name or self.name


class Journal(Named, Notable):
    '''List of associated journals for use with "book" objects'''
    pass


class Work(Notable):
    '''A platonic work.  Stores common information about multiple
    instances, copies, or editions of the same work.  Aggregates one
    or more :class:`Instance` objects.'''
    #: primary title
    primary_title = models.TextField()
    #: short title
    short_title = models.CharField(max_length=255)
    #: original publication date
    year = models.IntegerField(blank=True, null=True,
        help_text='Original publication date')
    # NOTE: this is inteneded for a generic linked data URI;
    # finding aid URL should be tracked on Instance rather than Work
    #: optional URI
    uri = models.URLField('URI', blank=True, help_text='Linked data URI',
        default='')
    #: relation to :class:`Person` authors
    authors = models.ManyToManyField(Person, blank=True)
    #: :class:`Subject` related through :class:`WorkSubject`
    subjects = models.ManyToManyField(Subject, through='WorkSubject')
    #: :class:`Language` related through :class:`WorkLanguage`
    languages = models.ManyToManyField(Language, through='WorkLanguage')

    class Meta:
        ordering = ['primary_title']
        verbose_name = 'Derrida library work'

    def __str__(self):
        return '%s (%s)' % (self.short_title, self.year or 'n.d.')

    def author_names(self):
        '''Display author names; convenience access for display in admin'''
        # NOTE: possibly might want to use last names here
        return ', '.join(str(auth) for auth in self.authors.all())
    author_names.short_description = 'Authors'
    author_names.admin_order_field = 'authors__authorized_name'

    def instance_count(self):
        base_url = reverse('admin:books_instance_changelist')
        return mark_safe('<a href="%s?%ss__id__exact=%s">%s</a>' % (
                            base_url,
                            self.__class__.__name__.lower(),
                            self.pk,
                            self.instance_set.count()
                ))
    instance_count.short_description = '# instances'


class InstanceQuerySet(models.QuerySet):
    '''Custom :class:`~django.db.models.QuerySet` for :class:`Instance` to
    make it easy to find all instances that have a digital
    edition'''

    def with_digital_eds(self):
        return self.exclude(digital_edition__isnull=True)


class Instance(Notable):
    '''A single instance of a :class:`Work` - i.e., a specific copy or edition
    or translation.  Can also include books that appear as sections
    of a collected works.'''

    #: :class:`Work` this instance belongs to
    work = models.ForeignKey(Work)
    #: alternate title (optional)
    alternate_title = models.CharField(blank=True, max_length=255)
    #: :class:`Publisher` (optional)
    publisher = models.ForeignKey(Publisher, blank=True, null=True)
    #: publication :class:`~derrida.places.models.Place` (optional, sorted many to many)
    pub_place = SortedManyToManyField(Place,
        verbose_name='Place(s) of Publication', blank=True)
    #: Zotero identifier
    zotero_id = models.CharField(
        max_length=255,
        # Add validator for any Zotero IDs entered manually by form.
        validators=[RegexValidator(
                        r'\W',
                        inverse_match=True,
                        message='Zotero IDs must be alphanumeric.'
                    )]
    )
    # identifying slug for use in get_absolute_url, indexed for speed
    slug = models.SlugField(max_length=255,
                            unique=True,
                            help_text=(
                                'To auto-generate a valid slug for a new '
                                'instance, choose a work then click '
                                '"Save and Continue Editing" in the lower '
                                'right. Editing slugs of previously saved '
                                'instances should be done with caution, '
                                'as this may break permanent links.'
                            ),
                            blank=True
    )

    #: item is extant
    is_extant = models.BooleanField(help_text='Extant in PUL JD', default=False)
    #: item is annotated
    is_annotated = models.BooleanField(default=False)
    #: item is translated
    is_translation = models.BooleanField(default=False)
    #: description of item dimensions (optional)
    dimensions = models.CharField(max_length=255, blank=True)
    #: copyright year
    copyright_year = models.PositiveIntegerField(blank=True, null=True)
    #: related :class:`Journal` for a journal article
    journal = models.ForeignKey(Journal, blank=True, null=True)
    print_date_help_text = 'Date as YYYY-MM-DD, YYYY-MM, or YYYY format. Use' \
        + ' print date day/month/year known flags to indicate' \
        + ' that the information is not known.'
    #: print date
    print_date = models.DateField('Print Date',
        blank=True, null=True, help_text=print_date_help_text)
    #: print date day is known
    print_date_day_known = models.BooleanField(default=False)
    #: print date month is known
    print_date_month_known = models.BooleanField(default=False)
    #: print date year is known
    print_date_year_known = models.BooleanField(default=True)
    #: finding aid URL
    uri = models.URLField('URI', blank=True, default='',
        help_text='Finding Aid URL for items in PUL Derrida Library')
    # item has a dedication
    has_dedication = models.BooleanField(default=False)
    # item has insertiosn
    has_insertions = models.BooleanField(default=False)
    # page range: using character fields to support non-numeric pages, e.g.
    # roman numerals for introductory pages; using two fields to support
    # sorting within a volume of collected works.
    #: start page for book section or journal article
    start_page = models.CharField(max_length=20, blank=True, null=True)
    #: end page for book section or journal article
    end_page = models.CharField(max_length=20, blank=True, null=True)
    #: optional label to distinguish multiple copies of the same work
    copy = models.CharField(max_length=1, blank=True,
        help_text='Label to distinguish multiple copies of the same edition',
        validators=[RegexValidator(r'[A-Z]',
            message='Please set a capital letter from A-Z.'
        )],
    )

    #: :class:`Language` this item is written in;
    # uses :class:`InstanceLanguage` to indicate primary language
    languages = models.ManyToManyField(Language, through='InstanceLanguage')

    #: :class:`Instance` that collects this item, for book section
    collected_in = models.ForeignKey('self', related_name='collected_set',
        on_delete=models.SET_NULL, blank=True, null=True,
        help_text='Larger work instance that collects or includes this item')
    # work instances are connected to owning institutions via the Catalogue
    # model; mapping as a many-to-many with a through
    # model in case we want to access owning instutions directly

    #: :class:`OwningInstitution`; connected through :class:`InstanceCatalogue`
    owning_institutions = models.ManyToManyField(OwningInstitution,
        through='InstanceCatalogue')

    #: :class:`DerridaWork` this item is cited in
    cited_in = models.ManyToManyField('DerridaWork',
        help_text='Derrida works that cite this edition or instance',
        blank=True)

    #: digital edition via IIIF as instance of :class:`djiffy.models.Manifest`
    digital_edition = models.OneToOneField(Manifest, blank=True, null=True,
        on_delete=models.SET_NULL,
        help_text='Digitized edition of this book, if available')

    #: flag to suppress content page images, to comply with copyright
    #: owner take-down request
    suppress_all_images = models.BooleanField(default=False,
        help_text='''Suppress large image display for all annotated pages
        in this volume, to comply with copyright take-down requests.
        (Overview images, insertions, and thumbnails will still display.)''')
    #: specific page images to be suppressed, to comply with copyright
    #: owner take-down request
    suppressed_images = models.ManyToManyField(Canvas, blank=True,
        help_text='''Suppress large image for specific annotated images to comply
        with copyright take-down requests.''')

    # proof-of-concept generic relation to footnotes
    #: generic relation to :class:~`derrida.footnotes.models.Footnote`
    footnotes = GenericRelation(Footnote)

    objects = InstanceQuerySet.as_manager()

    class Meta:
        ordering = ['alternate_title', 'work__primary_title'] ## ??
        verbose_name = 'Derrida library work instance'
        unique_together = (("work", "copyright_year", "copy"),)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_safe_slug()
        super(Instance, self).save(*args, **kwargs)

    def clean(self):
        # Don't allow both journal and collected work
        if self.journal and self.collected_in:
            raise ValidationError('Cannot belong to both a journal and a collection')

    def __str__(self):
        return '%s (%s%s)' % (self.display_title(),
            self.copyright_year or 'n.d.',
            ' %s' % self.copy if self.copy else '')

    def get_absolute_url(self):
        return reverse('books:detail', kwargs={'slug': self.slug})

    def generate_base_slug(self):
        '''Generate a slug based on first author, work title, and year.
        Not guaranteed to be unique if there are multiple copies of
        the same instance/edition of a work.

        :rtype str: String in the format ``lastname-title-of-work-year``
        '''
        # get the first author, if there is one
        author = self.work.authors.first()
        if author:
            # use the last name of the first author
            author = author.authorized_name.split(',')[0]
        else:
            # otherwise, set it to an empty string
            author = ''
        # truncate the title to first several words of the title
        title = ' '.join(self.work.primary_title.split()[:9])
        # use copyright year if available, with fallback to work year if
        year = self.copyright_year or self.work.year or ''
        # # return a slug (not unique for multiple copies of same instance)
        return slugify('%s %s %s' % (unidecode(author), unidecode(title), year))

    def generate_safe_slug(self):
        '''Generate a unique slug.  Checks for duplicates and calculates
        an appropriate copy letter if needed.

        :rtype str: String in the format `lastname-title-of-work-year-copy`
        '''

        # base slug, without any copy letter
        base_slug = self.generate_base_slug()
        if self.copy:
            slug = '-'.join([base_slug, self.copy])
        else:
            slug = base_slug

        # check for any copies with the same base slug
        duplicates = Instance.objects.filter(
            slug__icontains=base_slug).order_by('-slug')
        # exclude current record if it has already been saved
        if self.pk:
            duplicates = duplicates.exclude(pk=self.pk)
        # any new copies should start with 'B' since 'A' is implicit in already
        # saved slug for original
        new_copy_letter = 'B'
        # check for duplicates
        if duplicates.exists():
            # get the list of matching slugs
            slugs = duplicates.values_list('slug', flat=True)
            # if slug with specified copy is already unique, use that without
            # further processing
            if not slug in slugs:
                return slug

            # otherwise, calculate the appropriate copy letter to use

            # collect copy suffixes from the slugs
            # (trailing single uppercase letters only)
            letters = [ltr for slug in slugs
                       for ltr in slug.rsplit('-', 1)[1]
                       if len(ltr) == 1 and ltr in string.ascii_uppercase]

            # if existing copies letters are found, increment from the
            # highest one (already sorted properly from queryset return)
            if letters:
                next_copy = chr(ord(letters[0]) + 1)
            else:
                # otherwise, default next copy is B (first is assumed to be A)
                next_copy = 'B'
            slug = '-'.join([base_slug, next_copy])
            # also store the new copy letter as instance copy
            self.copy = next_copy

        return slug

    def display_title(self):
        '''display title - alternate title or work short title'''
        return self.alternate_title or self.work.short_title or '[no title]'
    display_title.short_description = 'Title'

    def is_digitized(self):
        '''boolean indicator if there is an associated digital edition'''
        return bool(self.digital_edition) or \
            bool(self.collected_in and self.collected_in.digital_edition)
    # technically sorts on the foreign key, but that effectively filters
    # instances with/without digital additions
    is_digitized.admin_order_field = 'digital_edition'
    is_digitized.boolean = True

    @property
    def location(self):
        '''Location in Derrida's library (currently only available for
        digitized books).'''
        # NOTE: PUL digital editions from the Finding Aid include the
        # location in the item title
        if self.is_digitized():
            # Split manifest label on dashes; at most we want the first two
            location_parts = self.digital_edition.label.split(' - ')[:2]
            # some volumes include a "Gift Books" notation we don't care about
            if location_parts[-1].startswith('Gift Books'):
                location_parts = location_parts[:-1]
            return ', '.join(location_parts)

    @property
    def item_type(self):
        '''item type: book, book section, or journal article'''
        if self.journal:
            return 'Journal Article'
        if self.collected_in:
            return 'Book Section'
        return 'Book'

    def author_names(self):
        '''Display Work author names; convenience access for display in admin'''
        return self.work.author_names()
    author_names.short_description = 'Authors'
    author_names.admin_order_field = 'work__authors__authorized_name'

    def catalogue_call_numbers(self):
        '''Convenience access to catalogue call numbers, for display in admin'''
        return ', '.join([c.call_number for c in self.instancecatalogue_set.all()
                          if c.call_number])
    catalogue_call_numbers.short_description = 'Call Numbers'
    catalogue_call_numbers.admin_order_field = 'catalogue__call_number'

    def print_year(self):
        '''Year from :attr:`print_date` if year is known'''
        if self.print_date and self.print_date_year_known:
            return self.print_date.year

    @property
    def year(self):
        '''year for indexing and display; :attr:`print_date` if known,
        otherwise :attr:`copyright_year`'''
        return self.print_year() or self.copyright_year

    def images(self):
        '''Queryset containing all :class:`djiffy.models.Canvas` objects
        associated with the digital edition for this item.'''
        if self.digital_edition:
            return self.digital_edition.canvases.all()
        return Canvas.objects.none()

    #: terms in an image label that indicate a canvas should be
    #: considered an overview image (e.g., cover & outside views)
    overview_labels = ['cover', 'spine', 'back', 'edge', 'view']

    def overview_images(self):
        '''Overview images for this book - cover, spine, etc.
        Filtered based on canvas label naming conventions.'''
        label_query = models.Q()
        for overview_label in self.overview_labels:
            label_query |= models.Q(label__icontains=overview_label)
        return self.images().filter(label_query) \
                   .exclude(label__icontains='insertion')

    def annotated_pages(self):
        '''Annotated pages for this book. Filtered based on the presence
        of a documented :class:`~derrida.interventions.models.Intervention`
        in the database.'''
        return self.images().filter(intervention__isnull=False).distinct()

    def insertion_images(self):
        '''Insertion images for this book.
        Filtered based on canvas label naming conventions.'''
        # NOTE: using Insertion because of possible case-sensitive
        # search on mysql even when icontains is used
        return self.images().filter(label__icontains='Insertion')

    @classmethod
    def allow_canvas_detail(cls, canvas):
        '''Check if canvas detail view is allowed.  Allows insertion images,
        overview images, and pages with documented interventions.'''
        return any([
            'insertion' in canvas.label.lower(),
            any(label in canvas.label.lower()
                for label in cls.overview_labels),
            canvas.intervention_set.exists()
        ])

    def allow_canvas_large_image(self, canvas):
        '''Check if canvas large image view is allowed.  Always allows
        insertion images and overview images; other pages with documented
        interventions are allowed as long as they are not suppressed,
        either via :attr:`suppress_all_images` or specific
        :attr:`suppressed_images`.'''
        # insertion & overview always allowed
        if any(['insertion' in canvas.label.lower(),
                any(label in canvas.label.lower()
                    for label in self.overview_labels)]):
            # allow
            return True
        # if all other images are suppressed, deny without checking further
        if self.suppress_all_images:
            return False
        # if image has interventions, check if it is suppressed
        if canvas.intervention_set.exists():
            # deny if suppressed
            if canvas in self.suppressed_images.all():
                return False
            else:
                # otherwise, allow
                return True

    @property
    def related_instances(self):
        '''Find related works; for now, this means works by the
        same author.  For a work that collects item, include
        work by any book section authors.'''
        authors = list(self.work.authors.all())
        exclude = [self.pk]
        if self.collected_set.exists():
            for instance in self.collected_set.all():
                authors.extend(instance.work.authors.all())

        return Instance.objects.filter(work__authors__in=authors) \
                       .exclude(pk=self.pk) \
                       .exclude(digital_edition__isnull=True)


class WorkSubject(Notable):
    '''Through-model for work-subject relationship, to allow designating
    a particular subject as primary or adding notes.'''
    #: :class:`Subject`
    subject = models.ForeignKey(Subject)
    #: :class:`Work`
    work = models.ForeignKey(Work)
    #: boolean flag indicating if this subject is primary for this work
    is_primary = models.BooleanField(default=False)

    class Meta:
        unique_together = ('subject', 'work')
        verbose_name = 'Subject'

    def __str__(self):
        return '%s %s%s' % (self.work, self.subject,
            ' (primary)' if self.is_primary else '')


class WorkLanguage(Notable):
    '''Through-model for work-language relationship, to allow designating
    one language as primary or adding notes.'''
    #: :class:`Language`
    language = models.ForeignKey(Language)
    #: :class:`Work`
    work = models.ForeignKey(Work)
    #: boolean flag indicating if this language is primary for this work
    is_primary = models.BooleanField()

    class Meta:
        unique_together = ('work', 'language')
        verbose_name = 'Language'

    def __str__(self):
        return '%s %s%s' % (self.work, self.language,
            ' (primary)' if self.is_primary else '')


class InstanceLanguage(Notable):
    '''Through-model for instance-language relationship, to allow designating
    one language as primary or adding notes.'''
    #: :class:`Language`
    language = models.ForeignKey(Language)
    #: :class:`Instance`
    instance = models.ForeignKey(Instance)
    #: boolean flag indicating if this language is primary for this instance
    is_primary = models.BooleanField()

    class Meta:
        unique_together = ('instance', 'language')
        verbose_name = 'Language'

    def __str__(self):
        return '%s %s%s' % (self.instance, self.language,
            ' (primary)' if self.is_primary else '')


class InstanceCatalogue(Notable, DateRange):
    '''Location of a work instance  in the real world, associating it with an
    owning instutition.'''
    institution = models.ForeignKey(OwningInstitution)
    instance = models.ForeignKey(Instance)
    is_current = models.BooleanField()
    # using char instead of int because assuming  call numbers may contain
    # strings as well as numbers
    call_number = models.CharField(max_length=255, blank=True, null=True,
        help_text='Used for Derrida shelf mark')

    class Meta:
        verbose_name = 'Catalogue'

    def __str__(self):
        dates = ''
        if self.dates:
            dates = ' (%s)' % self.dates
        return '%s / %s%s' % (self.instance, self.institution, dates)


class CreatorType(Named, Notable):
    '''Type of creator role a person can have to a book - author,
    editor, translator, etc.'''
    uri = models.URLField(blank=True, null=True)


class InstanceCreator(Notable):
    creator_type = models.ForeignKey(CreatorType)
    # technically should disallow author here, but can clean that up later
    person = models.ForeignKey(Person)
    instance = models.ForeignKey(Instance)

    def __str__(self):
        return '%s %s %s' % (self.person, self.creator_type, self.instance)


class PersonBookRelationshipType(Named, Notable):
    '''Type of non-annotation relationship assocating a person
    with a book.'''
    uri = models.URLField(blank=True, null=True)


class PersonBook(Notable, DateRange):
    '''Interactions or connections between books and people other than
    annotation.'''
    # FIXME: better name? concept/thing/model
    person = models.ForeignKey(Person)
    book = models.ForeignKey(Instance)
    relationship_type = models.ForeignKey(PersonBookRelationshipType)

    class Meta:
        verbose_name = 'Person/Book Interaction'

    def __str__(self):
        dates = ''
        if self.dates:
            dates = ' (%s)' % self.dates
        return '%s - %s%s' % (self.person, self.book, dates)


# New citationality model
class DerridaWork(Notable):
    '''This models the reference copy used to identify all citations, not
    part of Derrida's library'''
    #: short title
    short_title = models.CharField(max_length=255)
    #: full citation
    full_citation = models.TextField()
    #: boolean indicator for primary work
    is_primary = models.BooleanField()
    #: slug for use in URLs
    slug = models.SlugField(
        help_text='slug for use in URLs (changing after creation will break URLs)')

    def __str__(self):
        return self.short_title


class DerridaWorkSection(models.Model):
    '''Sections of a :class:`DerridaWork` (e.g. chapters). Used to look at
    :class:`Reference` by sections of the work.'''
    name = models.CharField(max_length=255)
    derridawork = models.ForeignKey(DerridaWork)
    order = models.PositiveIntegerField('Order')
    start_page = models.IntegerField(blank=True, null=True,
       help_text='Sections with no pages will be treated as headers.')
    end_page = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['derridawork', 'order']

    def __str__(self):
        return self.name


class ReferenceType(Named, Notable):
    '''Type of reference, i.e. citation, quotation, foonotes, epigraph, etc.'''
    pass


class ReferenceQuerySet(models.QuerySet):
    '''Custom :class:`~django.db.models.QuerySet` for :class:`Reference`.'''

    def order_by_source_page(self):
        '''Order by page in derrida work (attr:`Reference.derridawork_page`)'''
        return self.order_by('derridawork_page')

    def order_by_author(self):
        '''Order by author of cited work'''
        return self.order_by('instance__work__authors__authorized_name')

    def summary_values(self):
        '''Return a values list of summary information for display or
        visualization.  Currently used for histogram visualization.
        Author of cited work is aliased to `author`.
        '''
        return self.values('id', 'instance__slug', 'derridawork__slug',
            'derridawork_page', 'derridawork_pageloc',
           author=models.F('instance__work__authors__authorized_name'))


class Reference(models.Model):
    '''Reference to a book from a work by Derrida.  Can be a citation,
    quotation, or other kind of reference.'''
    #: :class:`Instance` that is referenced
    instance = models.ForeignKey(Instance, blank=True, null=True)
    #: :class:`DerridaWork` that references the item
    derridawork = models.ForeignKey(DerridaWork)
    #: page in the Derrida work.
    # FIXME: does this have to be char and not integer?
    derridawork_page = models.IntegerField()
    #: location/identifier on the page
    derridawork_pageloc = models.CharField(max_length=2)
    #: page in the referenced item
    book_page = models.CharField(max_length=255, blank=True)
    #: :class:`ReferenceType`
    reference_type = models.ForeignKey(ReferenceType)
    #: anchor text
    anchor_text = models.TextField(blank=True)
    #: ManyToManyField to :class:`djiffy.models.Canvas`
    canvases = models.ManyToManyField(Canvas, blank=True,
        help_text="Scanned images from Derrida's Library | ")
    #: ManyToManyField to :class:`derrida.interventions.Intervention`
    interventions = models.ManyToManyField('interventions.Intervention',
        blank=True)  # Lazy reference to avoid a circular import

    objects = ReferenceQuerySet.as_manager()

    class Meta:
        ordering = ['derridawork', 'derridawork_page', 'derridawork_pageloc']

    def __str__(self):
        return "%s, %s%s: %s, %s, %s" % (
            self.derridawork.short_title,
            self.derridawork_page,
            self.derridawork_pageloc,
            # instance is technically optional...
            self.instance.display_title() if self.instance else '[no instance]',
            self.book_page,
            self.reference_type
        )

    def get_absolute_url(self):
        '''URL for this reference on the site'''
        # NOTE: currently view is html snippet for loading via ajax only
        return reverse('books:reference', kwargs={
            'derridawork_slug': self.derridawork.slug,
            'page': self.derridawork_page,
            'pageloc': self.derridawork_pageloc
        })

    def anchor_text_snippet(self):
        '''Anchor text snippet, for admin display'''
        snippet = self.anchor_text[:100]
        if len(self.anchor_text) > 100:
            return ''.join([snippet, ' ...'])
        return snippet
    anchor_text_snippet.short_description = 'Anchor Text'
    anchor_text.admin_order_field = 'anchor_text'

    @property
    def instance_slug(self):
        '''Slug for the work instance used to display this reference.
        For a reference to a book section, returns the slug
        for the book that collects it.
        '''
        return self.book.slug

    @property
    def instance_url(self):
        '''absolute url for the work instance where this reference
        is displayed; uses :attr:`instance_slug`'''
        return reverse('books:detail', args=[self.instance_slug])

    @property
    def book(self):
        '''The "book" this reference is associated with; for a book section,
        this is the work instance the section is collected in; for all other
        cases, it is the work instance associated with this reference.
        '''
        if self.instance.collected_in:
            return self.instance.collected_in
        else:
            return self.instance

    @staticmethod
    def instance_ids_with_digital_editions():
        '''Used as a convenience method to provide a readonly field in the
        admin change form for :class:`Reference` with a list of JSON formatted
        primary keys. This is used by jQuery in the :class:`Reference`
        change_form and reference inlines on the :class:`Instance`change_form
        to disable the autocomplete fields when there is or is not a digital
        edition. See ``sitemedia/js/reference-instance-canvas-toggle.js`` for
        this logic.

        :rtype: JSON formatted string of :class:`Instance` primary keys
        '''
        with_digital_eds = Instance.objects.with_digital_eds()
        # Flatten to just the primary keys
        ids = with_digital_eds.values_list('id', flat=True).order_by('id')
        # Return serialized JSON
        return json.dumps(list(ids))
