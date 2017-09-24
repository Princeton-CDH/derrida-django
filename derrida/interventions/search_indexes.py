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
    text = indexes.CharField(document=True, use_template=True, stored=True)
    ### annotation details

    #: annotation or insertion (all annotation for now)
    intervention_type = indexes.CharField(model_attr='get_intervention_type_display')
    #: annotation type
    annotation_type = indexes.MultiValueField(faceted=True, null=True)
    #: annotation text
    annotation_text = indexes.CharField(model_attr='text', null=True)
    #: annotation anchor text
    anchor_text = indexes.CharField(model_attr='quote', null=True)
    #: annotation author
    annotation_author = indexes.CharField(faceted=True)

    annotation_language = indexes.CharField(model_attr='text_language',
            faceted=True, null=True)
    #: color ink or pencil of annotation
    ink = indexes.MultiValueField(faceted=True, null=True)
    #: thumbnail of the annotated page
    thumbnail = indexes.CharField(model_attr='canvas__image__thumbnail',
        null=True)
    #: cited work todo (canvas -> digital edition -> instance -> derrida work)

    ### annotated work details
    annotated_page = indexes.CharField(model_attr='canvas__label', null=True)
    # NOTE: using generic "item" to avoid confusion woth work, work instance, etc
    item_title = indexes.CharField(model_attr='work_instance__display_title')
    item_author = indexes.MultiValueField(model_attr='work_instance__work__authors__authorized_name',
        faceted=True)
    #: first author to allow sorting by author
    item_sort_author = indexes.CharField(model_attr='work_instance__work__authors__authorized_name',
        faceted=True)
    #: author in firstname last for display
    item_author_firstname_last = indexes.MultiValueField(model_attr='work_instance__work__authors__firstname_last')
    #: subject of annotated work
    item_subject = indexes.MultiValueField(model_attr='work_instance__work__subjects__name',
        faceted=True, null=True)
    #: language of publication
    item_language = indexes.MultiValueField(model_attr='work_instance__languages__name',
        faceted=True, null=True)
    #: original language
    item_work_language = indexes.MultiValueField(model_attr='work_instance__work__languages__name',
        faceted=True, null=True)
    #: edition year - is this populated? fallback to other dates?
    item_print_year = indexes.DecimalField(model_attr='work_instance__print_year', null=True)
    #: publication place
    item_pub_place = indexes.MultiValueField(model_attr='work_instance__pub_place__name',
        faceted=True, null=True)
    #: copy of edition
    item_copy = indexes.CharField(model_attr='work_instance__copy', null=True)
    #: slug for generating url to work
    item_slug = indexes.CharField(model_attr='work_instance__slug')

    def get_model(self):
        return Intervention

    def prepare_annotation_type(self, item):
        # get annotation types from the tags
        # TODO: may need to move into model class for shared display
        tags = [tag.name for tag in item.tags.all() if not any(
                 ['ink' in tag.name, 'pencil' in tag.name, 'uncertain' in tag.name,
                   'illegible' in tag.name])]
        if item.is_verbal():
            tags.append('verbal annotation')
        else:
            tags.append('nonverbal annotation')
        return tags

    def prepare_ink(self, item):
        # get pen and pencil types from the tags
        # TODO: may need to move into model class for shared display
        return [tag.name for tag in item.tags.all() if any(
                 ['ink' in tag.name, 'pencil' in tag.name])]

    def prepare_annotation_author(self, item):
        if item.author:
            return item.author.firstname_last
        else:
            return 'Unknown'
