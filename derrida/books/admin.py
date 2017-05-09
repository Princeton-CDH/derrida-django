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
            'reference_type',
            'anchor_text'
        )
        widgets = {
            'anchor_text': MeltdownTextAreaWidget(attrs={'class':
                                                         'grp-meltdown'}),
        }


class ReferenceInline(admin.StackedInline):
    '''Stacked inline for reference to give adequate room for the anchor_text
    editor'''
    model = Reference
    form = ReferenceModelForm
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


class ReferenceAdmin(admin.ModelAdmin):
    '''Override the modelform for Reference'''
    model = Reference
    form = ReferenceModelForm


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
    '''Inline for DerridaWork - Library Work relationships'''
    model = DerridaWorkBook
    extra = 1
    fields = ('derridawork', 'book', 'notes')


class BookAdmin(admin.ModelAdmin):
    '''Custom admin form for book, adds inlines and sets searchable fields, as
    well as general field order and list display modifications'''
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


admin.site.register(Subject,  NamedNotableBookCount)
admin.site.register(Language, NamedNotableBookCount)
admin.site.register(Publisher, NamedNotableBookCount)
admin.site.register(OwningInstitution, OwningInstitutionAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(CreatorType, NamedNotableAdmin)
admin.site.register(PersonBookRelationshipType, NamedNotableAdmin)
admin.site.register(PersonBook, PersonBookAdmin)

# Citationality sub module
admin.site.register(DerridaWork, DerridaWorkAdmin)
admin.site.register(ReferenceType)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(ItemType)
admin.site.register(Journal)
