from django import forms
from django.utils.safestring import mark_safe


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
    query = forms.CharField(label='Search', required=False)
    is_extant = forms.BooleanField(label="Extant in Derrida's Library",
        required=False)
    is_annotated = forms.BooleanField(label='Contains annotation',
        required=False)
    order_by = forms.ChoiceField(choices=[
            ('author', 'Author'),
            ('work_year', 'Publication date: oldest to newest'),
            ('-work_year', 'Publication date: newest to oldest'),
        ], required=False, initial='author',
        widget=forms.RadioSelect)

    facet_fields = ['author', 'subject', 'item_type', 'pub_place', 'language',
        'work_language', 'cited_in', 'author_letter']
    author = FacetChoiceField()
    subject = FacetChoiceField()
    language = FacetChoiceField('Language of Publication')
    work_language = FacetChoiceField('Original Language')
    pub_place = FacetChoiceField('Place of Publication')
    # TODO: work_year. range facet?
    item_type = FacetChoiceField(label='Publication Type')
    cited_in = FacetChoiceField()

    def set_choices_from_facets(self, facets):
        # configure field choices based on facets returned from Solr
        for facet, counts in facets.items():
            if facet in self.fields:
                self.fields[facet].choices = [
                    (val, mark_safe('%s <span>%d</span>' % (val, count)))
                    for val, count in counts]






