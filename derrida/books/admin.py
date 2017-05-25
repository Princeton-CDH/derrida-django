from django import forms
from django.contrib import admin
from dal import autocomplete

from derrida.common.admin import NamedNotableAdmin
from derrida.footnotes.admin import FootnoteInline
from .models import Subject, Language, Publisher, OwningInstitution, \
    Book, Catalogue, BookSubject, BookLanguage, CreatorType, Creator, \
    PersonBook, PersonBookRelationshipType, \
    DerridaWork, DerridaWorkBook, Reference, ReferenceType, Journal, ItemType, \
    AssociatedBook
# refactored models
from .models import Work, Instance, WorkSubject, WorkLanguage, \
    InstanceLanguage, InstanceCatalogue


class NamedNotableBookCount(NamedNotableAdmin):
    list_display = NamedNotableAdmin.list_display + ('book_count',)


class OwningInstitutionAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'place', 'has_notes', 'book_count')
    fields = ('name', 'short_name', 'contact_info', 'place', 'notes')
    search_fields = ('name', 'short_name', 'contact_info', 'notes')


class CollapsibleTabularInline(admin.TabularInline):
    'Django admin tabular inline with grappelli collapsible classes added'
    classes = ('grp-collapse grp-open',)


class CatalogueInline(CollapsibleTabularInline):
    model = Catalogue
    extra = 1
    fields = ('institution', 'call_number', 'start_year', 'end_year',
              'notes')


class SubjectInline(CollapsibleTabularInline):
    model = BookSubject
    extra = 1
    fields = ('subject', 'is_primary', 'notes')


class LanguageInline(CollapsibleTabularInline):
    model = BookLanguage
    extra = 1
    fields = ('language', 'is_primary', 'notes')

class CreatorInlineForm(forms.ModelForm):
    '''Custom model form for Book editing, used to add autocomplete
    for place lookup.'''
    class Meta:
        model = Creator
        fields = ('creator_type', 'person', 'notes')
        widgets = {
            'person': autocomplete.ModelSelect2(
                url='people:person-autocomplete',
                attrs={'data-placeholder': 'Start typing a name to search...'}
            )
        }


class CreatorInline(CollapsibleTabularInline):
    model = Creator
    extra = 1
    form = CreatorInlineForm


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


class ReferenceInline(admin.StackedInline):
    model = Reference
    extra = 1
    classes = ('grp-collapse grp-open',)
    fieldsets = (
        ('Citational Information', {
                'fields': (
                    'derridawork',
                    'derridawork_page',
                    'derridawork_pageloc',
                    'book_page',
                    'reference_type',
                )
        }),
        ('Anchor Text', {
            'fields': ('anchor_text',)
        }),
    )


class AssociatedBookInline(CollapsibleTabularInline):
    '''Tabular inline for Associated Book set'''
    model = AssociatedBook
    extra = 1
    fk_name = 'from_book'


class BookAdminForm(forms.ModelForm):
    '''Custom model form for Book editing, used to add autocomplete
    for place lookup.'''
    class Meta:
        model = Book
        exclude = []
        widgets = {
            'pub_place': autocomplete.ModelSelect2(
                url='places:autocomplete',
                attrs={'data-placeholder': 'Start typing location to search...'}),
           'publisher': autocomplete.ModelSelect2(
                url='books:publisher-autocomplete',
                attrs={'data-placeholder': 'Start typing publisher name to search...'})
        }


class DerridaWorkBookInline(CollapsibleTabularInline):
    model = DerridaWorkBook
    extra = 1
    fields = ('derridawork', 'book', 'notes')


class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm

    list_display = ('short_title', 'author_names', 'copyright_year',
        'catalogue_call_numbers', 'is_extant', 'is_annotated',
        'is_digitized', 'has_notes')
    # NOTE: fields are specified here so that notes input will be displayed last
    fields = ('primary_title', 'short_title', 'larger_work_title', 'item_type',
        'journal', 'original_pub_info', 'publisher',
        'pub_place', 'copyright_year', ('pub_date', 'pub_day_missing',
        'pub_month_missing'), 'is_extant', 'is_annotated', 'is_digitized', 'uri',
        'dimensions', 'notes')
    search_fields = ('primary_title', 'creator__person__authorized_name',
        'catalogue__call_number', 'notes', 'publisher__name')
    inlines = [AssociatedBookInline, DerridaWorkBookInline, ReferenceInline,
        CreatorInline, LanguageInline, SubjectInline, CatalogueInline,
        PersonBookInline, FootnoteInline]
    list_filter = ('subjects', 'languages', 'is_extant',
        'is_annotated', 'is_digitized')


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
    inlines = [DerridaWorkBookInline]
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
    list_display = ('short_title', 'author_names', 'year', 'instance_count', 'has_notes')
    # NOTE: fields are specified here so that notes input will be displayed last
    fields = ('primary_title', 'short_title', 'year', 'uri', 'authors', 'notes')
    search_fields = ('primary_title', 'authors__authorized_name', 'notes')
    inlines = [WorkSubjectInline, WorkLanguageInline, WorkInstanceInline]
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

class InstanceAdminForm(forms.ModelForm):
    '''Custom model form for Instance editing, used to add autocomplete
    for publication place  lookup.'''
    class Meta:
        model = Work
        exclude = []
        widgets = {
            'pub_place': autocomplete.ModelSelect2Multiple(
                url='places:autocomplete',
                attrs={'data-placeholder': 'Start typing location to search...'})
        }


class InstanceAdmin(admin.ModelAdmin):
    form = InstanceAdminForm

    list_display = ('display_title', 'author_names', 'copyright_year',
        'item_type', 'catalogue_call_numbers', 'is_extant', 'is_annotated',
        'is_translation', 'has_notes')
    # NOTE: fields are specified here so that notes input will be displayed last
    fields = ('work', 'alternate_title', 'journal', 'publisher',
        'pub_place', 'copyright_year', 'print_date',
        ('print_date_year_known', 'print_date_month_known',
         'print_date_day_known'),
        ('is_extant', 'is_translation'),
        ('is_annotated', 'has_insertions', 'has_dedication'),
        'uri', 'dimensions', ('start_page', 'end_page'),
        'collected_in', 'notes')
    search_fields = ('alternate_title', 'work__primary_title',
        'work__authors__authorized_name', 'instancecatalogue__call_number',
        'notes', 'publisher__name')
    # TODO: how to display sections collected by an instance?
    inlines = [InstanceLanguageInline, InstanceCatalogueInline, ReferenceInline]
    list_filter = ('languages', 'is_extant', 'is_annotated', 'has_insertions')


admin.site.register(Subject,  NamedNotableBookCount)
admin.site.register(Language, NamedNotableBookCount)
admin.site.register(Publisher, NamedNotableBookCount)
admin.site.register(OwningInstitution, OwningInstitutionAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(CreatorType, NamedNotableAdmin)
admin.site.register(PersonBookRelationshipType, NamedNotableAdmin)
admin.site.register(PersonBook, PersonBookAdmin)

# refactored models
admin.site.register(Work, WorkAdmin)
admin.site.register(Instance, InstanceAdmin)

# Citationality sub module
admin.site.register(DerridaWork, DerridaWorkAdmin)
admin.site.register(ReferenceType)
admin.site.register(Reference)
admin.site.register(ItemType)
admin.site.register(Journal)
