from django import forms
from django.utils.safestring import mark_safe

from derrida.books.forms import FacetChoiceField


class InterventionSearchForm(forms.Form):
    defaults = {
        'order_by': 'item_sort_author'
    }

    query = forms.CharField(label='Search', required=False)
    order_by = forms.ChoiceField(choices=[
            ('item_sort_author', 'Author of annotated work'),
            ('item_title', 'Title of annotated work'),
            # TODO: number of annotations?
        ], required=False, initial=defaults['order_by'],
        widget=forms.RadioSelect)

    # NOTE: currently these *must* match fields below *and*
    # valid fields in solr index or things will break
    facet_fields = ['item_author', 'item_subject', 'item_language',
        'item_work_language', 'item_pub_place', 'item_print_year',
        'annotation_language', 'annotation_type', 'annotation_author',
        'ink']
    item_author = FacetChoiceField()
    item_subject = FacetChoiceField()
    item_language = FacetChoiceField('Language of Publication')
    item_work_language = FacetChoiceField('Original Language')
    item_pub_place = FacetChoiceField('Place of Publication')
    item_print_year = FacetChoiceField('Edition Year')
    # TODO: work_year. range facet?
    annotation_language = FacetChoiceField('Annotation Language')
    annotation_type = FacetChoiceField('Annotation Type')
    annotation_author = FacetChoiceField('Annotation Hand')
    ink = FacetChoiceField(label='Ink')
    # TODO cited_in ?

    def set_choices_from_facets(self, facets):
        # configure field choices based on facets returned from Solr
        print(facets)
        for facet, counts in facets.items():
            if facet in self.fields:
                print('facet %s counts %s' % (facet, counts))
                self.fields[facet].choices = [
                    (val, mark_safe('%s <span>%d</span>' % (val, count)))
                    for val, count in counts]
