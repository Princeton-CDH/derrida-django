from dal import autocomplete, forward
from django import forms
from django.contrib import admin
from djiffy.admin import ManifestSelectWidget

from derrida.common.admin import NamedNotableAdmin
from derrida.footnotes.admin import FootnoteInline
from .models import Subject, Language, Publisher, OwningInstitution, \
    CreatorType, PersonBook, PersonBookRelationshipType, \
    DerridaWork, Reference, ReferenceType, Journal
# refactored models
from .models import Work, Instance, WorkSubject, WorkLanguage, \
    InstanceLanguage, InstanceCatalogue, InstanceCreator


class NamedNotableInstanceCount(NamedNotableAdmin):
    list_display = NamedNotableAdmin.list_display + ('instance_count',)


class NamedNotableWorkInstanceCount(NamedNotableAdmin):
    list_display = NamedNotableAdmin.list_display + \
        ('work_count', 'instance_count')

class NamedNotableWorkCount(NamedNotableAdmin):
    list_display = NamedNotableAdmin.list_display + ('work_count',)


class OwningInstitutionAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'place', 'has_notes', 'instance_count')
    fields = ('name', 'short_name', 'contact_info', 'place', 'notes')
    search_fields = ('name', 'short_name', 'contact_info', 'notes')


class CollapsibleTabularInline(admin.TabularInline):
    'Django admin tabular inline with grappelli collapsible classes added'
    classes = ('grp-collapse grp-open',)



class InstanceCreatorInlineForm(forms.ModelForm):
    '''Custom model form for Book editing, used to add autocomplete
    for place lookup.'''
    class Meta:
        model = InstanceCreator
        fields = ('creator_type', 'person', 'notes')
        widgets = {
            'person': autocomplete.ModelSelect2(
                url='people:person-autocomplete',
                attrs={'data-placeholder': 'Start typing a name to search...'}
            )
        }


class InstanceCreatorInline(CollapsibleTabularInline):
    model = InstanceCreator
    extra = 1
    form = InstanceCreatorInlineForm


class MeltdownTextAreaWidget(forms.Textarea):
    '''Adds Meltdown.js functionality and grp-meltdown to a text area and ensures
    all required js is loaded as well as a css fix to counteract an interaction
    between Grappelli and Meltdown.js.

    NOTE: Uses add-anchor-meltdown.js to initialize fields on the grp-meltdown
    class'''
    class Media:
        css = {
            'all': ('css/meltdown.css', 'css/meltdown-grappelli-fix.css',)
        }
        js = (
            'js/lib/js-markdown-extra.js',
            'js/jquery.meltdown.js',
            'js/lib/rangyinputs-jquery.min.js',
            'js/lib/element_resize_detection.js',
            'js/add-anchor-meltdown.js'
        )


class ReferenceModelForm(forms.ModelForm):
    '''Model form that uses custom Meltdownarea widget for anchor_text
    TextField'''
    class Meta:
        model = Reference
        fields = (
            'derridawork',
            'derridawork_page',
            'derridawork_pageloc',
            'book_page',
            'instance',
            'canvases',
            'interventions',
            'reference_type',
            'anchor_text',
        )
        widgets = {
            'anchor_text': MeltdownTextAreaWidget(attrs={'class':
                                                  'meltdown-widget'}),
            'canvases': autocomplete.ModelSelect2Multiple(
                url='djiffy:canvas-autocomplete',
                attrs={
                    'data-placeholder': 'Type a page or manifest label to '
                                        'search',
                    'data-width': '900px',
                },
                forward=[forward.Field('instance')],
            ),
            'interventions': autocomplete.ModelSelect2Multiple(
                url='interventions:autocomplete',
                attrs={
                    'data-placeholder': 'Type an intervention text or tag '
                                        '(exact) to search',
                    'data-width': '900px'
                },
                forward=[forward.Field('instance')],
            ),
        }


REFERENCE_LOOKUP_TEXT = ('<strong>Lookup is restricted to items associated'
                         ' with the digital edition for the referenced'
                         ' work. If the work has no digital edition,'
                         ' lookup is disabled.</strong>')

INSTANCE_ADDITION = ('<br /> <strong>Please add a digital edition and save'
                     ' first to enable editing.</strong>')

class ReferenceInline(admin.StackedInline):
    '''Stacked inline for reference to give adequate room for the anchor_text
    editor'''
    model = Reference
    form = ReferenceModelForm
    extra = 1
    classes = ('grp-collapse grp-open',)
    readonly_fields = ('get_autocomplete_instances', )
    fieldsets = (
        ('Citation Information', {
                'fields': (
                    'derridawork',
                    'derridawork_page',
                    'derridawork_pageloc',
                    'book_page',
                    'reference_type',
                )
        }),
        ('Interventions and Canvases', {
            'fields': (
                'canvases',
                'interventions',
                ),
            'description': REFERENCE_LOOKUP_TEXT + INSTANCE_ADDITION,
        }),
        ('Anchor Text', {
            'fields': ('anchor_text',)
        }),
    )
    widgets = {
            'anchor_text': MeltdownTextAreaWidget(attrs={'class':
                                                         'meltdown-widget'}),
        }


class ReferenceAdmin(admin.ModelAdmin):
    '''Customize admin display and editing for references.'''
    form = ReferenceModelForm
    list_display = ['derridawork', 'derridawork_page', 'derridawork_pageloc',
        'instance', 'book_page', 'reference_type', 'anchor_text_snippet']
    list_filter = ['derridawork', 'reference_type']
    search_fields = ['anchor_text']
    # *almost* the same as ReferenceInline.fieldsets (adds instance)
    readonly_fields = ('get_autocomplete_instances', )
    fieldsets = (
        ('Citation Information', {
                'fields': (
                    'derridawork',
                    'derridawork_page',
                    'derridawork_pageloc',
                    'instance',
                    'book_page',
                    'reference_type',
                )
        }),
        ('Interventions and Canvases', {
            'fields': (
                'canvases',
                'interventions',
                ),
            'description': REFERENCE_LOOKUP_TEXT,
        }),
        ('Anchor Text', {
            'fields': ('anchor_text',)
        }),
        # This field set provides hidden info for the reference admin to search
        # for instances by their primary key in jQuery as a hidden field and
        # applies a local CSS class to hide it.
        # NOTE: This field is a callable, so it can't be included in the
        # ModelForm so as to be given a HiddenInput
        ('Hidden Info', {
            'fields': ('get_autocomplete_instances', ),
            'classes': ('hidden-admin-info', ),
        })
    )

class PersonBookAdmin(admin.ModelAdmin):
    # NOTE: person-book is editable on the book page, but exposing as a
    # top level as well to make it easier to associate footnotes with
    # person-book relationships
    list_display = ('person', 'relationship_type', 'book', 'start_year',
                    'end_year', 'has_notes')
    fields = ('person', 'relationship_type', 'book', 'start_year',
              'end_year', 'notes')
    inlines = [FootnoteInline]


class DerridaWorkAdmin(admin.ModelAdmin):
    '''Creating a custom admin with inlines for Derrida Work to ease associating
    a specific book edition with it'''
    fields = ('short_title', 'full_citation', 'is_primary', 'notes')


### refactored work/instance model admin


class WorkSubjectInline(CollapsibleTabularInline):
    model = WorkSubject
    extra = 1
    fields = ('subject', 'is_primary', 'notes')


class WorkLanguageInline(CollapsibleTabularInline):
    model = WorkLanguage
    extra = 1
    fields = ('language', 'is_primary', 'notes')


class WorkInstanceInline(CollapsibleTabularInline):
    '''Minimal inline view to display instances within work edit form'''
    model = Instance
    extra = 0
    fields = ('alternate_title', 'copyright_year', 'print_date',
        'is_extant', 'is_annotated', 'is_translation', 'notes')
    # FIXME: this appears not to be supported by grappelli; how to work around?
    show_change_link = True


class WorkAdminForm(forms.ModelForm):
    '''Custom model form for Work editing, used to add autocomplete
    for person lookup.'''
    class Meta:
        model = Work
        exclude = []
        widgets = {
            'authors': autocomplete.ModelSelect2Multiple(
                url='people:person-autocomplete',
                attrs={'data-placeholder': 'Start typing a name to search...'}
            )
        }


class WorkAdmin(admin.ModelAdmin):
    form = WorkAdminForm
    list_display = ('short_title', 'author_names', 'year', 'instance_count',
        'has_notes')
    # NOTE: fields are specified here so that notes input will be displayed last
    fields = ('primary_title', 'short_title', 'year', 'uri', 'authors', 'notes')
    search_fields = ('primary_title', 'authors__authorized_name', 'notes')
    inlines = [WorkSubjectInline, WorkLanguageInline, WorkInstanceInline,
        FootnoteInline]
    list_filter = ('subjects', 'languages')


class InstanceLanguageInline(CollapsibleTabularInline):
    model = InstanceLanguage
    extra = 1
    fields = ('language', 'is_primary', 'notes')


class InstanceCatalogueInline(CollapsibleTabularInline):
    model = InstanceCatalogue
    extra = 1
    fields = ('institution', 'call_number', 'start_year', 'end_year',
              'notes')

class PersonBookInlineForm(forms.ModelForm):
    '''Custom model form for Book editing, used to add autocomplete
    for place lookup.'''
    class Meta:
        model = PersonBook
        fields = ('person', 'relationship_type', 'start_year', 'end_year',
                  'notes')
        widgets = {
            'person': autocomplete.ModelSelect2(
                url='people:person-autocomplete',
                attrs={'data-placeholder': 'Start typing a name to search...'}
            )
        }


class PersonBookInline(CollapsibleTabularInline):
    model = PersonBook
    extra = 1
    form = PersonBookInlineForm


class InstanceAdminForm(forms.ModelForm):
    '''Custom model form for Instance editing, used to add autocomplete
    for publication place lookup.'''
    # override print date field to allow entering just year or year-month
    print_date = forms.DateField(
            input_formats=["%Y", "%Y-%m", "%Y-%m-%d"],
            widget=forms.widgets.DateInput(format="%Y-%m-%d"),
            help_text=Instance.print_date_help_text,
            required=False)

    class Meta:
        model = Work
        exclude = []
        widgets = {
            'pub_place': autocomplete.ModelSelect2Multiple(
                url='places:autocomplete',
                attrs={'data-placeholder': 'Start typing location to search...'}),
           'digital_edition': ManifestSelectWidget
        }


class InstanceAdmin(admin.ModelAdmin):
    form = InstanceAdminForm
    # NOTE: uses custom change form to display associated interventions
    date_hierarchy = 'print_date'
    list_display = ('display_title', 'author_names', 'copyright_year',
        'item_type', 'catalogue_call_numbers', 'is_extant', 'is_annotated',
        'is_digitized', 'is_translation', 'has_notes')
    # NOTE: fields are specified here so that notes input will be displayed last
    fields = ('work', 'alternate_title', 'journal', 'publisher',
        'pub_place', 'copyright_year', 'print_date',
        ('print_date_year_known', 'print_date_month_known',
         'print_date_day_known'),
        ('is_extant', 'is_translation'),
        'cited_in',
        ('is_annotated', 'has_insertions', 'has_dedication'),
        'uri', 'dimensions', ('start_page', 'end_page'),
        'collected_in', 'digital_edition', 'notes')
    search_fields = ('alternate_title', 'work__primary_title',
        'work__authors__authorized_name', 'instancecatalogue__call_number',
        'notes', 'publisher__name', 'uri')
    # TODO: how to display sections collected by an instance?
    inlines = [ReferenceInline, InstanceCreatorInline, InstanceLanguageInline,
        InstanceCatalogueInline, PersonBookInline, FootnoteInline]
    list_filter = ('languages', 'is_extant', 'is_annotated', 'has_insertions')
    filter_horizontal = ['cited_in']


admin.site.register(Subject,  NamedNotableWorkCount)
admin.site.register(Language, NamedNotableWorkInstanceCount)
admin.site.register(Publisher, NamedNotableInstanceCount)
admin.site.register(OwningInstitution, OwningInstitutionAdmin)
# NOTE: suppress old book models from admin to avoid getting data
# entered in the wrong place; they will be removed in a subsequent release
# admin.site.register(Book, BookAdmin)
admin.site.register(CreatorType, NamedNotableAdmin)
# admin.site.register(PersonBookRelationshipType, NamedNotableAdmin)
# admin.site.register(PersonBook, PersonBookAdmin)

# refactored models
admin.site.register(Work, WorkAdmin)
admin.site.register(Instance, InstanceAdmin)

# Citationality sub module
admin.site.register(DerridaWork, DerridaWorkAdmin)
admin.site.register(ReferenceType)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Journal)
