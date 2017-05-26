from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.safestring import mark_safe
from sortedm2m.fields import SortedManyToManyField

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
    uri = models.URLField(blank=True, null=True)


class Language(Named, Notable, WorkCount, InstanceCount):
    '''Language that a book is written in or a language included in a book'''
    uri = models.URLField(blank=True, null=True)


class Publisher(Named, Notable, InstanceCount):
    '''Publisher of a book'''
    pass


class OwningInstitution(Named, Notable, InstanceCount):
    '''Institution that owns the extant copy of a book'''
    short_name = models.CharField(max_length=255, blank=True,
        help_text='Optional short name for admin display')
    contact_info = models.TextField()
    place = models.ForeignKey(Place)

    def __str__(self):
        return self.short_name or self.name


class ItemType(Named, Notable):
    '''Item types for types of book'''
    pass


class Journal(Named, Notable):
    '''List of associated journals for use with "book" objects'''
    pass

class Work(Notable):
    '''A platonic work.  Stores common information about multiple
    instances, copies, or editions of the same work.'''
    primary_title = models.TextField()
    short_title = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    # is this work-specific or instance?
    uri = models.URLField('URI', blank=True, help_text='Linked data URI',
        default='')
    authors = models.ManyToManyField(Person)
    subjects = models.ManyToManyField(Subject, through='WorkSubject')
    languages = models.ManyToManyField(Language, through='WorkLanguage')

    class Meta:
        ordering = ['primary_title']
        verbose_name = 'Derrida library work'

    def __str__(self):
        return '%s (%s)' % (self.short_title, self.year or 'n.d.')

    def author_names(self):
        'Display author names; convenience access for display in admin'
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


class Instance(Notable):
    '''A single instance of a work - i.e., a specific copy or edition
    or translation.  Can also include books that appear as sections
    of a collected works.'''
    work = models.ForeignKey(Work)
    alternate_title = models.CharField(blank=True, max_length=255)
    publisher = models.ForeignKey(Publisher, blank=True, null=True)
    pub_place = SortedManyToManyField(Place,
        verbose_name='Place(s) of Publication', blank=True)
    zotero_id = models.CharField(
        max_length=255,
        # Add validator for any Zotero IDs entered manually by form.
        validators=[RegexValidator(
                        r'\W',
                        inverse_match=True,
                        message='Zotero IDs must be alphanumeric.'
                    )]
    )
    is_extant = models.BooleanField(help_text='Extant in PUL JD', default=False)
    is_annotated = models.BooleanField(default=False)
    is_translation = models.BooleanField(default=False)
    dimensions = models.CharField(max_length=255, blank=True)
    copyright_year = models.PositiveIntegerField(blank=True, null=True)
    journal = models.ForeignKey(Journal, blank=True, null=True)
    print_date = models.DateField('Print Date',
        blank=True, null=True, help_text='Date in YYYY-MM-DD format. If either'
        ' pub_month or pub_day_missing are checked 01 for MM or DD indicates'
        ' that the information is not known.')
    print_date_day_known = models.BooleanField(default=False)
    print_date_month_known = models.BooleanField(default=False)
    print_date_year_known = models.BooleanField(default=True)
    uri = models.URLField('URI', blank=True, default='',
        help_text='Finding Aid URL for items in PUL Derrida Library')
    has_dedication = models.BooleanField(default=False)
    has_insertions = models.BooleanField(default=False)
    # page range: using character fields to support non-numeric pages, e.g.
    # roman numerals for introductory pages; using two fields to support
    # sorting within a volume of collected works.
    start_page = models.CharField(max_length=20, blank=True, null=True)
    end_page = models.CharField(max_length=20, blank=True, null=True)

    languages = models.ManyToManyField(Language, through='InstanceLanguage')

    collected_in = models.ForeignKey('self', related_name='collected_set',
        on_delete=models.SET_NULL, blank=True, null=True,
        help_text='Larger work instance that collects or includes this item')
    # work instances are connected to owning institutions via the Catalogue
    # model; mapping as a many-to-many with a through
    # model in case we want to access owning instutions directly
    owning_institutions = models.ManyToManyField(OwningInstitution,
        through='InstanceCatalogue')

    cited_in = models.ManyToManyField('DerridaWork',
        help_text='Derrida works that cite this edition or instance',
        blank=True)

    # proof-of-concept generic relation to footnotes
    footnotes = GenericRelation(Footnote)

    class Meta:
        ordering = ['alternate_title', 'work__primary_title'] ## ??
        verbose_name = 'Derrida library work instance'

    def clean(self):
        # Don't allow both journal and collected work
        if self.journal and self.collected_in:
            raise ValidationError('Cannot belong to both a journal and a collection')

    def __str__(self):
        return '%s (%s)' % (self.display_title(),
            self.copyright_year or 'n.d.')

    def display_title(self):
        return self.alternate_title or self.work.short_title or '[no title]'
    display_title.short_description = 'Title'

    @property
    def item_type(self):
        if self.journal:
            return 'Journal Article'
        if self.collected_in:
            return 'Book Section'
        return 'Book'

    def author_names(self):
        'Display Work author names; convenience access for display in admin'
        return self.work.author_names()
    author_names.short_description = 'Authors'
    author_names.admin_order_field = 'work__authors__authorized_name'

    def catalogue_call_numbers(self):
        'Convenience access to catalogue call numbers, for display in admin'
        return ', '.join([c.call_number for c in self.instancecatalogue_set.all()
                          if c.call_number])
    catalogue_call_numbers.short_description = 'Call Numbers'
    catalogue_call_numbers.admin_order_field = 'catalogue__call_number'


class WorkSubject(Notable):
    '''Through-model for work-subject relationship, to allow designating
    a particular subject as primary or adding notes.'''
    subject = models.ForeignKey(Subject)
    work = models.ForeignKey(Work)
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
    language = models.ForeignKey(Language)
    work = models.ForeignKey(Work)
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
    language = models.ForeignKey(Language)
    instance = models.ForeignKey(Instance)
    is_primary = models.BooleanField()

    class Meta:
        unique_together = ('instance', 'language')
        verbose_name = 'Language'

    def __str__(self):
        return '%s %s%s' % (self.instance, self.language,
            ' (primary)' if self.is_primary else '')


class Book(Notable):
    '''An individual book or volume, also journal articles and book sections'''
    primary_title = models.TextField()
    short_title = models.CharField(max_length=255)
    larger_work_title = models.TextField(blank=True, null=True)
    item_type = models.ForeignKey(ItemType)
    journal = models.ForeignKey(Journal, blank=True, null=True)
    page_range = models.CharField(max_length=20, blank=True, null=True)
    zotero_id = models.CharField(
        max_length=255,
        # Add validator for any Zotero IDs entered manually by form.
        validators=[RegexValidator(
                        r'\W',
                        inverse_match=True,
                        message='Zotero IDs must be alphanumeric.'
                    )]
    )
    original_pub_info = models.TextField(
        verbose_name='Original Publication Information',
        blank=True,
        null=True,
        )
    publisher = models.ForeignKey(Publisher, blank=True, null=True)
    pub_place = models.ForeignKey(Place, verbose_name='Place of Publication',
        blank=True, null=True)
    # New date field model for Derrida to accomodate work dates and
    # French copyright/printing practices.
    pub_date = models.DateField('Publication/Print Date',
        blank=True, null=True, help_text='Date in YYYY-MM-DD format. If either'
        ' pub_month or pub_day_missing are checked 01 for MM or DD indicates'
        ' that the information is not known.')
    pub_month_missing = models.BooleanField(default=False)
    pub_day_missing = models.BooleanField(default=False)
    # This is possibly suboptimal  but I'm going to be using flags so I can write this
    # as a field set and specify how to handle the date using the Quincy project
    # as an example.
    copyright_year = models.PositiveIntegerField(blank=True, null=True)
    work_year = models.IntegerField(blank=True, null=True)
    # is positive integer enough, or do we need more validation here?
    is_extant = models.BooleanField(help_text='Extant in PUL JD', default=False)
    is_annotated = models.BooleanField(default=False)
    is_digitized = models.BooleanField(default=False)
    is_translation = models.BooleanField(default=False)
    has_insertions = models.BooleanField(default=False)
    has_dedication = models.BooleanField(default=False)
    dimensions = models.CharField(max_length=255, blank=True)
    # expected length? is char sufficient or do we need text?
    # Finding Aid url
    uri = models.URLField(help_text='Finding Aid URL', blank=True, null=True)
    subjects = models.ManyToManyField(Subject, through='BookSubject')
    languages = models.ManyToManyField(Language, through='BookLanguage')
    books = models.ManyToManyField('Book', through='AssociatedBook')

    # books are connected to owning institutions via the Catalogue
    # model; mapping as a many-to-many with a through
    # model in case we want to access owning instutions directly
    owning_institutions = models.ManyToManyField(OwningInstitution,
        through='Catalogue')

    # proof-of-concept generic relation to footnotes
    # (actual models that need this still TBD)
    footnotes = GenericRelation(Footnote)

    class Meta:
        ordering = ['primary_title']
        verbose_name = 'Derrida library work (OLD)'
        verbose_name_plural = 'Derrida library works (OLD)'

    def __str__(self):
        return '%s (%s)' % (self.short_title, self.copyright_year or 'n.d.')

    def catalogue_call_numbers(self):
        'Convenience access to catalogue call numbers, for display in admin'
        return ', '.join([c.call_number for c in self.catalogue_set.all()
                          if c.call_number])
    catalogue_call_numbers.short_description = 'Call Numbers'

    def authors(self):
        return self.creator_set.filter(creator_type__name='Author')

    def author_names(self):
        'Display author names; convenience access for display in admin'
        # NOTE: possibly might want to use last names here
        return ', '.join(str(auth.person) for auth in self.authors())
    author_names.short_description = 'Authors'
    author_names.admin_order_field = 'creator__person__authorized_name'

    def add_author(self, person):
        '''Add the specified person as an author of this book'''
        self.add_creator(person, 'Author')

    def add_editor(self, person):
        '''Add the specified person as an editor of this book'''
        self.add_creator(person, 'Editor')

    def add_translator(self, person):
        '''Add the specified person as an translator of this book'''
        self.add_creator(person, 'Translator')

    def add_creator(self, person, creator_type):
        '''Associate the specified person as a creator of this book
        using the specified type (e.g., author, editor, etc.).
        Will throw an exception if creator type is not valid.'''
        creator_type = CreatorType.objects.get(name=creator_type)
        Creator.objects.create(person=person, creator_type=creator_type,
            book=self)

    def get_parent(self):
        '''Returns the physical parent book for a section. If called on a parent,
        returns None for a falsy value.'''
        parent = None
        if self.item_type.name == 'Book':
            return None
        else:
            associated_books = AssociatedBook.objects.filter(
                (Q(from_book=self) or Q(to_book=self)) and Q(is_collection=True)
            )
            for association in associated_books:
                if association.from_book.item_type.name == 'Book':
                    parent = association.from_book
                else:
                    parent = association.to_book
        return parent

    def get_children(self):
        '''Returns children of a parent book. If called on a child, returns None
        so can be used as a children property check'''
        children = []
        # Using list in case we encounter book types that need to be added.
        if self.item_type.name not in ['Book']:
            return None
        else:
            associated_books = AssociatedBooks.objects.filter(
                (Q(from_book=self) or Q(to_book=self)) and Q(is_collection=True)
            )
            for association in associated_books:
                if association.from_book.item_type not in ['Book']:
                    children.append(association.from_book)
                if association.to_book.item_type not in ['Book']:
                    children.append(association.to_book)
        return children

    def save(self, *args, **kwargs):
        '''Override save for this model to set date-month based on flags'''
        if self.pub_day_missing:
            self.pub_date = self.pub_date.replace(day=1)
        if self.pub_month_missing:
            self.pub_date = self.pub_date.replace(month=1)
        super(Book, self).save(*args, **kwargs);



class AssociatedBook(models.Model):
    '''Through model for associated book sets or sections'''
    from_book = models.ForeignKey(Book, related_name='from_book')
    to_book = models.ForeignKey(
        Book,
        related_name='to_book',
        help_text=('Creates associations between works. To edit an existing'
                   ' instance, please delete the relationship and'
                   ' make a new one')
    )
    # Makes sure that this relationship is a physical collection with book sections
    is_collection = models.BooleanField(
        default=False,
        help_text=('Denotes that a BookSection/Book or other section/work '
                   'relationship is an actual parent-child. Assumes parent '
                   'is larger work even though relationship is symmetric.')
    )

    class Meta:
        verbose_name = 'Associated Book'

    def __str__(self):
        return '%s - %s' % (self.from_book.short_title, self.to_book.short_title)


class Catalogue(Notable, DateRange):
    '''Location of a book in the real world, associating it with an
    owning instutition.'''
    institution = models.ForeignKey(OwningInstitution)
    book = models.ForeignKey(Book)
    is_current = models.BooleanField()
    # using char instead of int because assuming  call numbers may contain
    # strings as well as numbers
    call_number = models.CharField(max_length=255, blank=True, null=True,
        help_text='Used for Derrida shelf mark')



    def __str__(self):
        dates = ''
        if self.dates:
            dates = ' (%s)' % self.dates
        return '%s / %s%s' % (self.book, self.institution, dates)


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



class BookSubject(Notable):
    '''Through-model for book-subject relationship, to allow designating
    a particular subject as primary or adding notes.'''
    subject = models.ForeignKey(Subject)
    book = models.ForeignKey(Book)
    is_primary = models.BooleanField()

    class Meta:
        unique_together = ('subject', 'book')

    def __str__(self):
        return '%s %s%s' % (self.book, self.subject,
            ' (primary)' if self.is_primary else '')


class BookLanguage(Notable):
    '''Through-model for book-language relationship, to allow designating
    one language as primary or adding notes.'''
    language = models.ForeignKey(Language)
    book = models.ForeignKey(Book)
    is_primary = models.BooleanField()

    class Meta:
        unique_together = ('book', 'language')

    def __str__(self):
        return '%s %s%s' % (self.book, self.language,
            ' (primary)' if self.is_primary else '')


class CreatorType(Named, Notable):
    '''Type of creator role a person can have to a book - author,
    editor, translator, etc.'''
    uri = models.URLField(blank=True, null=True)
    pass


class Creator(Notable):
    creator_type = models.ForeignKey(CreatorType)
    person = models.ForeignKey(Person)
    book = models.ForeignKey(Book)

    def __str__(self):
        return '%s %s %s' % (self.person, self.creator_type, self.book)


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
    short_title = models.CharField(max_length=255)
    full_citation = models.TextField()
    is_primary = models.BooleanField()
    cited_books = models.ManyToManyField(
        'Book',
        through='DerridaWorkBook',
        help_text='Indicate which edition(s) of a book Derrida '
                  'cites in this work.',
    )

    def __str__(self):
        return self.short_title


class DerridaWorkBook(Notable):
    '''Allows Book (now <Work>) model to be associated with the Platonic
    DerridaWork model to indicate which physical books he is citing'''
    derridawork = models.ForeignKey(
        DerridaWork,
        verbose_name='Cited in'
    )
    book = models.ForeignKey(
        Book,
         verbose_name='Cited edition',
    )

    class Meta:
        verbose_name = 'Edition - Derrida work relation'
        verbose_name_plural = 'Edition - Derrida work relations'

    def __str__(self):
        return 'Derrida cites %s in %s' % (self.book, self.derridawork)


class ReferenceType(Named, Notable):
    '''Type of reference, i.e. citation, quotation, foonotes, epigraph, etc.'''
    pass


class Reference(models.Model):
    '''References to Derrida's works from Zotero Tags collected by team'''
    book = models.ForeignKey(Book)
    # reference both book and instance until book data is migrated
    instance = models.ForeignKey(Instance, blank=True, null=True)
    derridawork = models.ForeignKey(DerridaWork)
    derridawork_page = models.CharField(max_length=10)
    derridawork_pageloc = models.CharField(max_length=2)
    book_page = models.CharField(max_length=255, blank=True)
    reference_type = models.ForeignKey(ReferenceType)
    anchor_text = models.TextField(blank=True)

    class Meta:
        ordering = ['derridawork', 'derridawork_page', 'derridawork_pageloc']


    def __str__(self):
        return "%s, %s%s: %s, %s, %s" % (
            self.derridawork.short_title,
            self.derridawork_page,
            self.derridawork_pageloc,
            self.book.short_title,
            self.book_page,
            self.reference_type
        )

    def anchor_text_snippet(self):
        '''Anchor text snippet, for admin display'''
        snippet = self.anchor_text[:100]
        if len(self.anchor_text) > 100:
            return ''.join([snippet, ' ...'])
        return snippet
    anchor_text_snippet.short_description = 'Anchor Text'
    anchor_text.admin_order_field = 'anchor_text'
