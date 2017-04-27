from django import forms
from django.contrib import admin
from django.conf import settings
from django.utils.safestring import mark_safe
from dal import autocomplete

from derrida.footnotes.admin import FootnoteInline
from .models import Person, Residence, RelationshipType, Relationship


class RelationshipInlineForm(forms.ModelForm):
    '''Custom model form for Book editing, used to add autocomplete
    for place lookup.'''
    class Meta:
        model = Relationship
        template = 'admin/relationship_custom_inline.html'
        # Setting a logical order for the relationship fields
        fields = ('relationship_type', 'to_person', 'start_year',
            'end_year', 'notes')
        widgets = {
            'to_person': autocomplete.ModelSelect2(
                url='people:person-autocomplete',
                attrs={'data-placeholder': 'Start typing a name to search...'}
            )
        }


class RelationshipInline(admin.TabularInline):
    '''Inline class for Relationships'''
    model = Relationship
    fk_name = 'from_person'
    form = RelationshipInlineForm
    verbose_name_plural = 'From Relationships'
    extra = 1


class ResidenceInline(admin.TabularInline):
    '''Inline class for Residence'''
    model = Residence
    extra = 1
    # Setting a logical order for the residence fields
    fields = ('place', 'start_year', 'end_year', 'notes')


class ViafWidget(autocomplete.Select2):
    '''Customize autocomplete select widget to display VIAF id as a link'''
    # (inspired by winthrop.places.admin.GeoNamesWidget)

    def render(self, name, value, attrs=None):
        widget = super(ViafWidget, self).render(name, value, attrs)
        return mark_safe(
            u'%s<p><br /><a id="viaf_uri" target="_blank" href="%s">%s</a></p>'
            '<p> Note: Choosing a VIAF value will automatically set the birth'
            ' and death fields, blanking the input if there is a previous value.') % \
            (widget, value or '', value or '')


class PersonAdminForm(forms.ModelForm):
    '''Custom model form for Person editing, used to add VIAF lookup'''
    class Meta:
        model = Person
        exclude = []
        widgets = {
                'viaf_id': ViafWidget(
                    url='people:viaf-autosuggest',
                    attrs={
                        'data-placeholder': 'Type a name to search VIAF',
                        'data-minimum-input-length': 3
                    }
                )
        }



class PersonAdmin(admin.ModelAdmin):
    form = PersonAdminForm
    inlines = [
        FootnoteInline, ResidenceInline, RelationshipInline
    ]
    list_display = ('authorized_name', 'sort_name', 'birth', 'death',
        'viaf_id', 'family_group')
    list_filter = ('family_group',)
    fields = ('authorized_name', 'sort_name', 'viaf_id', ('birth', 'death'),
        'family_group', 'notes')
    search_fields = ('authorized_name',)

    class Media:
        static_url = getattr(settings, 'STATIC_URL')
        js = ['admin/viaf-suggest.js']

admin.site.register(Person, PersonAdmin)
admin.site.register(RelationshipType)
