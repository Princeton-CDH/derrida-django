from haystack import indexes
from derrida.books.models import Instance, Reference, DerridaWork
import roman


# Solr index needs to support:
# Browse/search library books cited in DG
# - Display thumbnail, title, author, year and copy
# - Filter by date range, cited/not
# - Sort by author, publication date

class InstanceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, stored=False)
    #: display title of book; :class:`derrida.books.models.Instance.display_title`
    display_title = indexes.CharField(model_attr='display_title', faceted=True)
    #: sortable field for display title
    display_title_isort = indexes.CharField(model_attr='display_title')
    #: item type; :class:`derrida.books.models.Instance.item_type`
    item_type = indexes.CharField(model_attr='item_type', faceted=True)
    #: copy letter, if any; :class:`derrida.books.models.Instance.copy`
    copy = indexes.CharField(model_attr='copy', null=True)
    #: author names in lastname, first for sort/facet; :class:`derrida.books.models.Work.authors`
    author = indexes.MultiValueField(model_attr='work__authors__authorized_name',
        faceted=True, null=True)
    #: non-multifield for first author to allow sorting by author
    author_isort = indexes.CharField(null=True)
    #: author in firstname last for display; :class:`derrida.books.models.Work.authors`
    author_firstname_last = indexes.MultiValueField(model_attr='work__authors__firstname_last',
        null=True)
    #: subjects associated with Instance; :class:`derrida.books.models.Work.subjects`
    subject = indexes.MultiValueField(model_attr='work__subjects__name',
        faceted=True, null=True)
    #: languages associated with Instance; :class:`derrida.books.models.Instance.languages`
    language = indexes.MultiValueField(model_attr='languages__name',
        faceted=True, null=True)
    #: place of publication; :class:`derrida.books.models.Instance.pub_place`
    pub_place = indexes.MultiValueField(model_attr='pub_place__name',
        faceted=True, null=True)
    #: original work languages; :class:`derrida.books.models.Work.languages`
    work_language = indexes.MultiValueField(model_attr='work__languages__name',
        faceted=True, null=True)
    #: original work year; :class:`derrida.books.models.Work.year`
    work_year = indexes.IntegerField(model_attr='work__year', null=True)
    #: copyright year of Instance; :class:`derrida.books.models.Instance.copyright_year`
    copyright_year = indexes.IntegerField(model_attr='copyright_year', null=True)
    #: print year of Instance; :class:`derrida.books.models.Instance.print_year`
    print_year = indexes.IntegerField(model_attr='print_year', null=True)
    #: sort/display year: print year if known; otherwise, copyright year.
    year = indexes.IntegerField(model_attr='year', null=True)
    #: gives work of Derrida (DerridaWork) in which this Instance is cited
    cited_in = indexes.MultiValueField(faceted=True, null=True)
    #: whether the Instance is extant; :class:`derrida.books.models.Instance.is_extant`
    is_extant = indexes.FacetBooleanField(model_attr='is_extant')
    #: whether the Instance has annotations by Derrida; :class:`derrida.books.models.Instance.is_annotated`
    is_annotated = indexes.FacetBooleanField(model_attr='is_annotated')
    #: whether the Instance is digitized; :class:`derrida.books.models.Instance.digital_edition`
    digital_edition = indexes.FacetBooleanField(model_attr='digital_edition')
    #: the instance's url slug; :class:`derrida.books.models.Instance.slug`
    slug = indexes.CharField(model_attr='slug')

    def get_model(self):
        return Instance

    def prepare_author_isort(self, instance):
        '''Return first author for author sort field.'''
        first_author = instance.work.authors.first()
        if first_author:
            return first_author.authorized_name

    def prepare_cited_in(self, instance):
        '''Return Derridaworks in which this instance is cited.'''
        # return cited work once only;
        # check for references to this instance or any book sections
        # it collects
        ref_ids = [ref.id for ref in instance.reference_set.all()]
        ref_ids.extend([ref.id for bksect in instance.collected_set.all()
                        for ref in bksect.reference_set.all()])
        # use distinct to avoid needless repetition
        return [dw.short_title for dw in
                DerridaWork.objects.filter(reference__in=ref_ids).distinct()]


class ReferenceIndex(indexes.SearchIndex, indexes.Indexable):
    '''Search index instance for :class:`derrida.books.models.Reference`'''
    text = indexes.CharField(document=True, use_template=True, stored=False)
    #: Short title for search form from :class:`~derrida.books.models.DerridaWork`
    derridawork = indexes.CharField(model_attr='derridawork__short_title', faceted=True)
    #: Name value for the :class:`~derrida.books.models.ReferenceType` of citation
    reference_type = indexes.CharField(model_attr='reference_type__name',
        faceted=True)
    #: Page in derrida work; :attr:`derrida.books.models.Reference.derridawork_page`
    derridawork_page = indexes.IntegerField(model_attr='derridawork_page')
    #: Page location in derrida work; :attr:`derrida.books.models.Reference.derridawork_pageloc`
    derridawork_pageloc = indexes.CharField(model_attr='derridawork_pageloc')
    #: derrida work slug in derrida work; :attr:`derrida.books.models.DerridaWork.slug`
    derridawork_slug = indexes.CharField(model_attr='derridawork__slug')
    #: Cited page in referenced work; :attr:`derrida.books.models.Reference.book_page`
    book_page = indexes.CharField(model_attr='book_page', null=True, faceted=True)
    #: sort field for reference work page to sort page numbers correctly
    book_page_sort = indexes.IntegerField()
    #: anchor text
    anchor_text = indexes.CharField(model_attr='anchor_text', null=True)
    #: ids for corresponding intervention
    interventions = indexes.MultiValueField(model_attr='interventions__id')
    #: has corresponding intervention
    corresponding_intervention = indexes.FacetBooleanField()
    #: canvas id for detail page view, if view available for book page
    page_canvas_id = indexes.CharField(null=True)
    # - related instance and work info
    #: Title of instance to which citation points; :meth:`derrida.books.models.Instance.display_title`
    instance_title = indexes.CharField(model_attr='instance__display_title',
        faceted=True)
    instance_title_isort = indexes.CharField(model_attr='instance__display_title')
    #: Instance authors for faceted filtering
    instance_author = indexes.MultiValueField(model_attr='instance__work__authors__authorized_name',
        faceted=True, null=True)
    #: Instance authors for display
    instance_author_firstname_last = indexes.MultiValueField(model_attr='instance__work__authors__firstname_last',
        null=True)
    #: non-multifield for instance first author to allow sorting by author
    instance_author_isort = indexes.CharField(model_attr='instance__work__authors__authorized_name',
        null=True)
    #: subjects for associated instance; :attr:`derrida.books.models.Instance.subjects`
    instance_subject = indexes.MultiValueField(model_attr='instance__work__subjects__name',
        faceted=True, null=True)
    #: languages for associated instance; :attr:`derrida.book.models.Instance.languages`
    instance_language = indexes.MultiValueField(faceted=True, null=True)
    #: languages for the original work; :attr:`derrida.book.models.Work.languages`
    original_language = indexes.MultiValueField(model_attr='instance__work__languages__name',
        faceted=True)
    instance_pub_place = indexes.MultiValueField(model_attr='book__pub_place__name',
        faceted=True, null=True)
    #: work year of the associated instance's work; :attr:`derrida.books.models.Work.year`
    instance_work_year = indexes.IntegerField(model_attr='instance__work__year', null=True)
    #: copyright year of associated instance; :attr:`derrida.books.models.Instance.copyright_year`
    instance_copyright_year = indexes.IntegerField(model_attr='instance__copyright_year', null=True)
    #: print year of associated instance; :attr:`derrida.books.models.Instance.r_year`
    instance_print_year = indexes.IntegerField(model_attr='instance__print_year', null=True)
    #: is instance extant in PU collection?; :attr:`derrida.books.models.Instance.is_extant`
    instance_is_extant = indexes.FacetBooleanField(model_attr='book__is_extant')
    #: is instance annotated?; :attr:`derrida.books.models.Instance.is_annotated`
    instance_is_annotated = indexes.FacetBooleanField(model_attr='book__is_annotated')
    #: instance slug, for generating urls and filtering by instance
    instance_slug = indexes.CharField(model_attr='book__slug')
    #: instance copy, for distinguishing multiple copies of the same edition
    instance_copy = indexes.CharField(model_attr='book__copy', null=True)
    #: boolean indicating if instance has digital edition
    instance_digital_edition = indexes.FacetBooleanField(model_attr='book__digital_edition')
    #: instance collection title, for references to book sections
    instance_collection_title = indexes.CharField(model_attr='instance__collected_in__display_title',
        null=True)

    def get_model(self):
        return Reference

    def prepare_instance_author_isort(self, reference):
        '''Return first author for author sort field.'''
        first_author = reference.instance.work.authors.first()
        if first_author:
            return first_author.authorized_name

    def prepare_corresponding_intervention(self, reference):
        '''
        Return whether :class:`derrida.books.models.Reference` has a
        corresponding :class:`derrida.interventions.models.Intervention`.
        '''
        return bool(reference.interventions.count())

    def prepare_page_canvas_id(self, reference):
        '''
        Return canvas short_id for first associated
        :class:`derrida.interventions.models.Intervention`.
        '''
        if reference.interventions.exists():
            # don't error on intervention without canvas
            # (probably only exists in test data)
            if reference.interventions.first().canvas:
                return reference.interventions.first().canvas.short_id

    def prepare_instance_language(self, reference):
        '''
        Return language of :class:`derrida.books.models.Reference`'s associated
        :class:`derrida.books.models.Instannce`.
        '''
        # use languages directly on this instance, if available (even if a
        # book section or article)
        if reference.instance.languages.exists():
            return [lang.name for lang in reference.instance.languages.all()]
        # if no languages directly set and part of a collected work, use
        # collection work languages
        if reference.instance.collected_in:
            return [lang.name for lang in reference.instance.collected_in.languages.all()]

    def prepare_book_page_sort(self, reference):
        '''
        Handle integer values and sort in page references, as well as Roman
        numerals from introductions.
        '''
        # if empty immediately return 0 for no sort
        if not reference.book_page:
            return 0
        book_page = reference.book_page.lower()
        # ignore any back references to derridawork citation, e.g. (256a)
        book_page = book_page.split(')')[-1]
        # split on '-' if it exists; just get first page of page range
        book_page = book_page.split('-')[0]
        # strip any trailing p or s
        book_page = book_page.strip('ps')

        # try converting to integer - should work in most cases
        try:
            return int(book_page)
        except ValueError:
            pass

        # if that fails, check for a roman numeral
        try:
            # return a negative number so front matter pages (up to 500)
            # will sort before pages with regular numbers.
            return roman.fromRoman(book_page.upper()) - 500
        except roman.InvalidRomanNumeralError:
            pass

        # if no conversion succeeded, return zero
        return 0
