# import datetime
import re
from haystack import indexes
from derrida.books.models import Instance, Reference


# Solr index needs to support:
# Browse/search library books cited in DG
# - Display thumbnail, title, author, year and copy
# - Filter by date range, cited/not
# - Sort by author, publication date

class InstanceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, stored=False)
    display_title = indexes.CharField(model_attr='display_title', faceted=True)
    item_type = indexes.CharField(model_attr='item_type', faceted=True)
    copy = indexes.CharField(model_attr='copy', null=True)
    #: author names in lastname, first for sort/facet
    author = indexes.MultiValueField(model_attr='work__authors__authorized_name',
        faceted=True)
    #: non-multifield for first author to allow sorting by author
    sort_author = indexes.CharField(model_attr='work__authors__authorized_name',
        faceted=True)
    #: author in firstname last for display
    author_firstname_last = indexes.MultiValueField(model_attr='work__authors__firstname_last')
    subject = indexes.MultiValueField(model_attr='work__subjects__name',
        faceted=True, null=True)
    language = indexes.MultiValueField(model_attr='languages__name',
        faceted=True, null=True)
    pub_place = indexes.MultiValueField(model_attr='pub_place__name',
        faceted=True, null=True)
    work_language = indexes.MultiValueField(model_attr='work__languages__name',
        faceted=True, null=True)
    work_year = indexes.IntegerField(model_attr='work__year', null=True)
    copyright_year = indexes.IntegerField(model_attr='copyright_year', null=True)
    print_year = indexes.IntegerField(model_attr='print_year', null=True)
    #: sort/display year: print year if known; otherwise, copyright year.
    year = indexes.IntegerField(model_attr='year', null=True)
    # FIXME: a book is cited if items it collects are cited
    cited_in = indexes.MultiValueField(model_attr='reference_set__derridawork__short_title',
        faceted=True, null=True)
    is_extant = indexes.FacetBooleanField(model_attr='is_extant')
    is_annotated = indexes.FacetBooleanField(model_attr='is_annotated')
    digital_edition = indexes.FacetBooleanField(model_attr='digital_edition')
    slug = indexes.CharField(model_attr='slug')

    def get_model(self):
        return Instance


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
    # - related instance and work info
    #: Title of instance to which citation points; :method:`derrida.books.models.Instance.display_title`
    instance_title = indexes.CharField(model_attr='instance__display_title',
        faceted=True)
    #: Instance authors for faceted filtering
    instance_author = indexes.MultiValueField(model_attr='instance__work__authors__authorized_name',
        faceted=True)
    #: Instance authors for display
    instance_author_firstname_last = indexes.MultiValueField(model_attr='instance__work__authors__firstname_last')
    #: non-multifield for instance first author to allow sorting by author
    instance_sort_author = indexes.CharField(model_attr='instance__work__authors__authorized_name',
        faceted=True)
    #: subjects for associated instance; :attr:`derrida.books.models.Instance.subjects`
    instance_subject = indexes.MultiValueField(model_attr='instance__work__subjects__name',
        faceted=True, null=True)
    #: languages for associated instance; :attr:`derrida.book.models.Instance.languages`
    instance_language = indexes.MultiValueField(model_attr='instance__languages__name',
        faceted=True, null=True)
    #: languages for the original work; :attr:`derrida.book.models.Work.languages`
    original_language = indexes.MultiValueField(model_attr='instance__work__languages__name',
        faceted=True)
    instance_pub_place = indexes.MultiValueField(model_attr='instance__pub_place__name',
        faceted=True, null=True)
    #: copyright year of associated instance; :attr:`derrida.books.models.Instance.copyright_year`
    instance_copyright_year = indexes.DecimalField(model_attr='instance__copyright_year', null=True)
    #: print year of associated instance; :attr:`derrida.books.models.Instance.print_year`
    instance_print_year = indexes.DecimalField(model_attr='instance__print_year', null=True)
    #: is instance extant in PU collection?; :attr:`derrida.books.models.Instance.is_extant`
    instance_is_extant = indexes.FacetBooleanField(model_attr='instance__is_extant')
    #: is instance annotated?; :attr:`derrida.books.models.Instance.is_annotated`
    instance_is_annotated = indexes.FacetBooleanField(model_attr='instance__is_annotated')
    #: instance slug, for generating urls and filtering by instance
    instance_slug = indexes.CharField(model_attr='instance_slug')
    #: instance copy, for distinguishing multiple copies of the same edition
    instance_copy = indexes.CharField(model_attr='instance__copy', null=True)
    #: boolean indicating if instance has digital edition
    instance_digital_edition = indexes.FacetBooleanField(model_attr='instance__digital_edition')

    def get_model(self):
        return Reference

    def prepare_instance_sort_author(self, reference):
        first_author = reference.instance.work.authors.first()
        if first_author:
            return first_author.authorized_name

    def prepare_corresponding_intervention(self, reference):
        return reference.interventions.count()

    def prepare_book_page_sort(self, reference):
        '''Handle integer values and sort in page references'''
        # if empty immediately return 0 for no sort
        if not reference.book_page:
            return 0
        book_page = reference.book_page
        # strip back references to derridawork citation, i.e. (256a)
        book_page = re.sub(r'\(.*\)', '', book_page)
        # split on '-' if it exists
        book_page = book_page.split('-')[0]
        # strip p and s and upper
        book_page = book_page.strip('ps').upper()
        # check for a roman numeral
        if not re.search(r'[^MDCLXVI]+', book_page):
            roman_nums = {
                'M': 1000, 'D': 500, 'C': 100,
                'L': 50, 'X': 10, 'V': 5, 'I': 1
            }
            value = 0
            previous = ''
            for char in book_page:
                # first letter is always added
                if not previous:
                    value = roman_nums[char]
                if previous:
                    # add a smaller number
                    if roman_nums[previous] >= roman_nums[char]:
                        value += roman_nums[char]
                    # if a larger follows a smaller, it will be one place value
                    # off (i.e. 9 instead of 10, 90 instead of 100, etc.)
                    # so we can deduct counting it previously and then subtract
                    # it again from value of the following character
                    if roman_nums[previous] < roman_nums[char]:
                        value += (roman_nums[char] - roman_nums[previous]*2)
                previous = char
            # This results in front matter pages (up to 500) being indexed
            # before regular pages.
            return value - 500
        # remove any other non-numeric characters for irregular references
        book_page = re.sub(r'[^1-9]', '', book_page)
        # return the characters as an integer
        if book_page:
            return int(book_page)
        # if blank string, return zero (no sort)
        return 0
