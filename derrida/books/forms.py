from django import forms
from django.utils.safestring import mark_safe


class SearchForm(forms.Form):
    defaults = {
        'content_type': 'all',
    }
    query = forms.CharField(label='Search Terms...', required=False)

    content_type = forms.ChoiceField(choices=[
        ('all', 'All'),
        ('book', 'Books'),
        ('reference', 'References'),
        ('intervention', 'Interventions'),
    ], required=False, initial=defaults['content_type'])


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
        # NOTE: restricting here hides a couple of volumes;
        # is this a data error or something else?
        # 'cited_in': ['De la grammatologie']
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

    # input fields that wrap a solr facet
    facet_inputs = ['author', 'subject', 'language', 'work_language',
        'pub_place', 'cited_in']

    def set_choices_from_facets(self, facets):
        # configure field choices based on facets returned from Solr
        for facet, counts in facets.items():
            if facet in self.fields:
                self.fields[facet].choices = [
                    (val, mark_safe('%s <span>%d</span>' % (val, count)))
                    for val, count in counts]

    def solr_field(self, field):
        '''Return corresponding solr field for search facet or order
        input for this form.'''
        # sort fields
        if field in self.sort_fields:
            return self.sort_fields[field]

        # facets
        # (currently all input names match facets)
        if field in self.facet_fields:
            return field


class ReferenceSearchForm(forms.Form):
    defaults = {
        'order_by': 'dw_page',
        'derridawork': ['De la grammatologie']
    }
    query = forms.CharField(label='Search', required=False)

    order_by = forms.ChoiceField(choices=[
            ('dw_page', 'Page order in Derrida work'),
            ('cited_author', 'Author of cited work'),
            ('cited_title', 'Title of cited work'),
        ], required=False, initial=defaults['order_by'],
        widget=forms.RadioSelect)

    #: order options and corresponding solr field
    sort_fields = {
        'dw_page': 'derridawork_page',
        'cited_author': 'instance_sort_author_exact',
        'cited_title': 'instance_title_exact',
    }
    # fields to request facets from solr
    facet_fields = ['derridawork', 'reference_type', 'instance_author',
        'instance_subject', 'instance_language', 'original_language',
        'instance_pub_place']
        #'pub_language', 'orig_language']. # range facets TODO

    # map solr facet field to corresponding form input
    solr_facet_fields = {
        'instance_author': 'author',
        'instance_subject': 'subject',
        'instance_language': 'language',
        'instance_pub_place': 'pub_place',
    }
    # input fields that wrap a solr facet
    facet_inputs = ['derridawork', 'reference_type', 'author', 'subject',
        'language', 'original_language', 'pub_place']

    is_extant = forms.BooleanField(label="Extant in Derrida's Library",
        required=False)
    is_annotated = forms.BooleanField(label='Contains annotation',
        required=False)
    corresponding_intervention = forms.BooleanField(label='Contains corresponding annotation',
        required=False)
    author = FacetChoiceField(label='Author')
    subject = FacetChoiceField(label='Subject')
    language = FacetChoiceField(label='Language of Publication')
    original_language = FacetChoiceField(label='Original Language')
    pub_place = FacetChoiceField(label='Place of Publication')
    # TODO: original pub year, edition year, print year
    reference_type = FacetChoiceField(label='Reference Type', required=False)
    derridawork = FacetChoiceField(label='Cited by Derrida in', required=False)

    def set_choices_from_facets(self, facets):
        # configure field choices based on facets returned from Solr
        # TODO: Generalize this for a sublcass of forms.Form?
        for facet, counts in facets.items():
            formfield = self.solr_facet_fields.get(facet, facet)
            if formfield in self.fields:
                self.fields[formfield].choices = [
                    (val, mark_safe('%s <span>%d</span>' % (val, count)))
                    for val, count in counts]

    def solr_field(self, field):
        '''Return corresponding solr field for search facet or order
        input for this form.'''
        # sort fields
        if field in self.sort_fields:
            return self.sort_fields[field]

        # facets
        if field in self.facet_fields:
            return field

        if field in self.solr_facet_fields.values():
            # currently all are instance_field, but generate
            # based on the dictionary in case that changes
            for key, value in self.solr_facet_fields.items():
                if value == field:
                    return key



class SuppressImageForm(forms.Form):
    '''Simple form for admin request to suppress a single
    canvas image or all annotated pages from a volume.'''
    suppress = forms.ChoiceField(choices=[
            ('current', 'this page'),
            ('all', 'all annotated pages in this volume'),
        ], initial='current', widget=forms.RadioSelect)
    canvas_id = forms.CharField(widget=forms.HiddenInput)
