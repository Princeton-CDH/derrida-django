from django.contrib import admin


class NamedNotableAdmin(admin.ModelAdmin):
    '''Generic model admin for named/notable models.'''
    list_display = ('name', 'has_notes')
    # fields = ('name', 'notes')
    search_fields = ('name', 'notes')
