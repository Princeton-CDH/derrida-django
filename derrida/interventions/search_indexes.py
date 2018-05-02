from haystack import indexes
from derrida.interventions.models import Intervention

# Solr index needs to support:
# Browse/search interventions
# - Display cited page thumbnail, title, author, year and copy
# - Filter by annotated work fields:
#      author, subject, language of publication, original language,
#      edition year,
# - Filter on annotation details: language, annotation type, annotation hand,
#   ink, cited in Derrida work (?)
# - Sort by author of annotated work, title of annotated work,
#   number of annotations (?)


class InterventionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, stored=False)
    ### annotation details

    #: annotation or insertion (all annotation for now); display value for :class:`derrida.interventions.models.Intervention.intervention_type`
    intervention_type = indexes.CharField(model_attr='get_intervention_type_display')
    #: annotation type; :class:`derrida.interventions.models.Intervention.annotation_type`
    annotation_type = indexes.MultiValueField(model_attr='annotation_type',
        faceted=True, null=True)
    #: annotation text; :class:`derrida.interventions.models.Intervention.text`
    annotation_text = indexes.CharField(model_attr='text', null=True)
    #: language code for annotation text language
    annotation_text_lang = indexes.CharField(model_attr='text_language__code', null=True)
    #: annotation anchor text; :class:`derrida.interventions.models.Intervention.quote`
    anchor_text = indexes.CharField(model_attr='quote', null=True)
    #: language code for anchor text language
    anchor_text_lang = indexes.CharField(model_attr='quote_language__code', null=True)
    #: annotation author
    annotation_author = indexes.CharField(faceted=True, null=True)
    #: annotation text's language; :class:`derrida.interventions.models.Intervention.text_language`
    annotation_language = indexes.CharField(model_attr='text_language',
            faceted=True, null=True)
    #: color ink or pencil of annotation; :class:`derrida.interventions.Intervention.ink`
    ink = indexes.MultiValueField(model_attr='ink', faceted=True, null=True)
    #: thumbnail of the annotated page;
    thumbnail = indexes.CharField(model_attr='canvas__image__thumbnail',
        null=True)
    #: cited work todo (canvas -> digital edition -> instance -> derrida work)

    ### annotated work details
    annotated_page = indexes.CharField(model_attr='canvas__label', null=True)
    # NOTE: using generic "item" to avoid confusion woth work, work instance, etc
    #: title of item; :class:`derrida.books.Instance.display_title`
    item_title = indexes.CharField(model_attr='work_instance__display_title')
    #: sortable title field
    item_title_isort = indexes.CharField(model_attr='work_instance__display_title')
    item_author = indexes.MultiValueField(model_attr='work_instance__work__authors__authorized_name',
        faceted=True, null=True)
    #: first author to allow sorting by author
    item_author_isort = indexes.CharField(model_attr='work_instance__work__authors__authorized_name',
        null=True)
    #: author in firstname last for display
    item_author_firstname_last = indexes.MultiValueField(model_attr='work_instance__work__authors__firstname_last',
        null=True)
    #: subject of annotated work; :class:`derrida.books.models.Work.subjects`
    item_subject = indexes.MultiValueField(model_attr='work_instance__work__subjects__name',
        faceted=True, null=True)
    #: language of publication; :class:`derrida.books.models.Instance.languages`
    item_language = indexes.MultiValueField(model_attr='work_instance__languages__name',
        faceted=True, null=True)
    #: original language; class:`derrida.books.models.Work.languages`
    item_work_language = indexes.MultiValueField(model_attr='work_instance__work__languages__name',
        faceted=True, null=True)
    # TODO: is this populated? fallback to other dates?
    #: edition year; :class:`derrida.books.models.Instance.print_year`
    item_print_year = indexes.IntegerField(model_attr='work_instance__print_year', null=True)
    #: work publication year; :class:`derrida.books.models.Work.year`
    item_work_year = indexes.IntegerField(model_attr='work_instance__work__year', null=True)
    #: work copyright year; :class:`derrida.books.models.Instance.copyright_year`
    item_copyright_year = indexes.IntegerField(model_attr='work_instance__copyright_year', null=True)
    #: publication place; :class:`derrida.books.models.Instance.pub_place`
    item_pub_place = indexes.MultiValueField(model_attr='work_instance__pub_place__name',
        faceted=True, null=True)
    #: copy of edition; :class:`derrida.books.models.Instance.copy`
    item_copy = indexes.CharField(model_attr='work_instance__copy', null=True)
    #: slug for generating url to work; :class:`derrida.books.models.Instance.slug`
    item_slug = indexes.CharField(model_attr='work_instance__slug')

    # canvas details
    canvas_id = indexes.CharField(model_attr='canvas__short_id')

    def get_model(self):
        return Intervention

    def index_queryset(self, using=None):
        # exclude any interventions on canvases that are not associated
        # with a work instance (work instance data is needed to be meaningful)
        qs = super(InterventionIndex, self).index_queryset(using)
        return qs.exclude(canvas__manifest__instance__isnull=True)

    def prepare_annotation_author(self, item):
        '''Return firstname, last of annotation author.'''
        if item.author:
            return item.author.firstname_last
        else:
            return 'Unknown'
