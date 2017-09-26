# import datetime
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
    author_letter = indexes.MultiValueField(faceted=True)
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
    year = indexes.IntegerField(null=True)
    cited_in = indexes.MultiValueField(model_attr='reference_set__derridawork__short_title',
        faceted=True, null=True)
    is_extant = indexes.FacetBooleanField(model_attr='is_extant')
    is_annotated = indexes.FacetBooleanField(model_attr='is_extant')
    digital_edition = indexes.FacetBooleanField(model_attr='digital_edition')
    slug = indexes.CharField(model_attr='slug')

    # FIXME: probably shouldn't use this in production because it
    # could expose the actual plum image url, which should be hidden
    # to protect the content
    # TODO: make a local view to proxy instead?
    thumbnail = indexes.CharField(model_attr='digital_edition__thumbnail__image__thumbnail',
        null=True)

    def get_model(self):
        return Instance

    def prepare_author_letter(self, instance):
        # first letter of author
        return [author.authorized_name[0].upper() for author in instance.work.authors.all()]

    def prepare_year(self, instance):
        # sort/display year: print year if known; otherwise, copyright year.
        return instance.print_year() or instance.copyright_year


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
    #: Cited page in referenced work; :attr:`derrida.books.models.Reference.book_page`
    book_page = indexes.CharField(model_attr='book_page', null=True)
    #: anchor text
    anchor_text = indexes.CharField(model_attr='anchor_text', null=True)
    # - related instance and work info
    #: Title of instance to which citation points; :method:`derrida.books.models.Instance.display_title`
    instance_title = indexes.CharField(model_attr='instance__display_title')
    #: Instance authors for faceted filtering; :method:`derrida.books.models.Work.firstname_last`
    instance_author = indexes.MultiValueField(model_attr='instance__work__authors__firstname_last')
    #: author in firstname last for display
    instance_author_letter = indexes.MultiValueField(faceted=True)
    #: subjects for associated instance; :attr:`derrida.books.models.Instance.subjects`
    instance_subject = indexes.MultiValueField(model_attr='instance__work__subjects__name',
        faceted=True, null=True)
    #: languages for associated instance; :attr:`derrida.book.models.Instance.languages`
    instance_language = indexes.MultiValueField(model_attr='instance__languages__name',
        faceted=True, null=True)
    #: languages for the original work; :attr:`derrida.book.models.Work.languages`
    original_language = indexes.MultiValueField(model_attr='instance__work__languages__name')
    #: copyright year of associated instance; :attr:`derrida.books.models.Instance.copyright_year`
    instance_copyright_year = indexes.DecimalField(model_attr='instance__copyright_year', null=True)
    #: print year of associated instance; :attr:`derrida.books.models.Instance.print_year`
    instance_print_year = indexes.DecimalField(model_attr='instance__print_year', null=True)
    #: is instance extant in PU collection?; :attr:`derrida.books.models.Instance.is_extant`
    instance_is_extant = indexes.FacetBooleanField(model_attr='instance__is_extant')
    #: is instance annotated?; :attr:`derrida.books.models.Instance.is_annotated`
    instance_is_annotated = indexes.FacetBooleanField(model_attr='instance__is_annotated')
    #: instance slug, for generating urls and filtering by instance
    instance_slug = indexes.CharField(model_attr='instance__slug')

    def get_model(self):
        return Reference

    def prepare_instance_author_letter(self, instance):
        # first letter of author
        # slightly odd notation of instance.instance is correct here
        return [author.authorized_name[0].upper()
                for author in instance.instance.work.authors.all()]
