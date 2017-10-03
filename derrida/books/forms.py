from django import forms
from django.utils.safestring import mark_safe


class SearchForm(forms.Form):
    query = forms.CharField(label='Search Terms...', required=False)
    content_type = forms.ChoiceField(choices=[
        ('all', 'All'),
        ('book', 'Books'),
        ('reference', 'References'),
        ('intervention', 'Interventions'),
    ], required=False, initial='all')


class FacetChoiceField(forms.MultipleChoiceField):
    # customize multiple choice field for use with facets
    # - turn of choice validation (shouldn't fail if facets don't get loaded)
    # - default to not required
    # - use checkbox select multiple as default widget

    widget = forms.CheckboxSelectMultiple

    def __init__(self, *args, **kwargs):
        if 'required' not in kwargs:
            kwargs['required'] = False
        super(FacetChoiceField, self).__init__(*args, **kwargs)

    def valid_value(self, value):
        return True


class InstanceSearchForm(forms.Form):
    defaults = {
        'order_by': 'author',
        # TODO
        # 'cited_in': 'de la grammatologie'
    }

    query = forms.CharField(label='Search', required=False)
    is_annotated = forms.BooleanField(label='Contains annotation',
        required=False)

    order_by = forms.ChoiceField(choices=[
            ('author', 'Author'),
            ('title', 'Title'),
            ('oldest', 'Publication date: oldest to newest'),
            ('newest', 'Publication date: newest to oldest'),
        ], required=False, initial=defaults['order_by'],
        widget=forms.RadioSelect)

    #: order options and corresponding solr field
    sort_fields = {
        'author': 'sort_author',
        'title': 'display_title_exact',
        'oldest': 'year',
        'newest': '-year'
    }

    facet_fields = ['author', 'subject', 'item_type', 'pub_place', 'language',
        'work_language', 'cited_in']
    author = FacetChoiceField()
    subject = FacetChoiceField()
    language = FacetChoiceField('Language of Publication')
    work_language = FacetChoiceField('Original Language')
    pub_place = FacetChoiceField('Place of Publication')
    # TODO: work_year. range facet?
    # item_type = FacetChoiceField(label='Publication Type')
    cited_in = FacetChoiceField()


    def set_choices_from_facets(self, facets):
        # configure field choices based on facets returned from Solr
        for facet, counts in facets.items():
            if facet in self.fields:
                self.fields[facet].choices = [
                    (val, mark_safe('%s <span>%d</span>' % (val, count)))
                    for val, count in counts]


class ReferenceSearchForm(forms.Form):

    query = forms.CharField(label='Search', required=False)

    facet_fields = ['derridawork', 'reference_type']

    instance_is_extant = forms.BooleanField(label="Extant in Derrida's Library",
        required=False)
    instance_is_annotated = forms.BooleanField(label='Contains annotation',
        required=False)
    derridawork = FacetChoiceField(label='Cited by Derrida in', required=False)
    reference_type = FacetChoiceField(label='Citation Type', required=False)
    instance_author = FacetChoiceField(label='Publication Author')
    instance_subject = FacetChoiceField(label='Publication Subject')
    instance_language = FacetChoiceField(label='Language of Publication')
    original_language = FacetChoiceField(label='Original Language')

    def set_choices_from_facets(self, facets):
        # configure field choices based on facets returned from Solr
        # TODO: Generalize this for a sublcass of forms.Form?
        for facet, counts in facets.items():
            if facet in self.fields:
                self.fields[facet].choices = [
                    (val, mark_safe('%s <span>%d</span>' % (val, count)))
                    for val, count in counts]


class SuppressImageForm(forms.Form):
    '''Simple form for admin request to suppress a single
    canvas image or all annotated pages from a volume.'''
    suppress = forms.ChoiceField(choices=[
            ('current', 'this page'),
            ('all', 'all annotated pages in this volume'),
        ], initial='current', widget=forms.RadioSelect)
    canvas_id = forms.CharField(widget=forms.HiddenInput)
