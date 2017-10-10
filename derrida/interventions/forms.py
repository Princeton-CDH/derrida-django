from django import forms
from django.utils.safestring import mark_safe

from derrida.books.forms import FacetChoiceField


class InterventionSearchForm(forms.Form):
    defaults = {
        'order_by': 'author'
    }

    query = forms.CharField(label='Search', required=False)
    order_by = forms.ChoiceField(choices=[
            ('author', 'Author of annotated work'),
            ('title', 'Title of annotated work'),
            # TODO: number of annotations?
        ], required=False, initial=defaults['order_by'],
        widget=forms.RadioSelect)

    #: order options and corresponding solr field
    sort_fields = {
        'author': 'item_sort_author_exact',
        'title': 'item_title',
    }

    # fields to request facets from solr
    facet_fields = ['item_author', 'item_subject', 'item_language',
        'item_work_language', 'item_pub_place', # 'item_print_year',
        'annotation_language', 'annotation_type', 'annotation_author',
        'ink']

    # input fields that wrap a solr facet
    facet_inputs = ['author', 'subject', 'language', 'work_language',
        'pub_place', 'annotation_language', 'annotation_type',
        'hand', 'ink']

    author = FacetChoiceField()
    subject = FacetChoiceField()
    language = FacetChoiceField('Language of Publication')
    work_language = FacetChoiceField('Original Language')
    pub_place = FacetChoiceField('Place of Publication')
    # print_year = FacetChoiceField('Edition Year')
    # TODO: work_year. range facet?
    annotation_language = FacetChoiceField('Annotation Language')
    annotation_type = FacetChoiceField('Annotation Type')
    hand = FacetChoiceField('Annotation Hand')
    ink = FacetChoiceField(label='Ink')
    # TODO cited_in ?

    # map solr facet field to corresponding form input
    solr_facet_fields = {
        'item_author': 'author',
        'item_subject': 'subject',
        'item_language': 'language',
        'item_work_language': 'work_language',
        'item_pub_place': 'pub_place',
        'item_print_year': 'print_year',
        'annotation_author': 'hand',
    }


    def set_choices_from_facets(self, facets):
        # configure field choices based on facets returned from Solr
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
