from annotator_store.admin import AnnotationAdmin
from dal import autocomplete
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from djiffy.models import Canvas

from .models import Intervention, Tag


class CanvasLinkWidget(autocomplete.ModelSelect2):
    '''Customize autocomplete select widget to include a link
    to view the related canvas on the website, since the 'view on site'
    link for an annotation resolves to the JSON API url.'''

    class Media:
        css = {
            'all': ('css/local-admin.css',)
        }

    def render(self, name, value, attrs=None):
        widget = super(CanvasLinkWidget, self).render(name, value, attrs)
        # if no canvas id is set, return widget as is
        if not value:
            return widget

        # otherwise, add a link to view the canvas on the site;
        # borrowing grappelli style for main "view on site" button
        canvas = Canvas.objects.get(id=value)
        return mark_safe(u'''%s
            <ul class="canvas-link grp-object-tools">
                <li><a href="%s" target="_blank" class="grp-state-focus">View canvas on site</a>
            </li></ul>''' % (widget, canvas.get_absolute_url()))



class InterventionAdminForm(forms.ModelForm):
    '''Custom model form for Intervention editing; used to configure
    autocomplete lookups.'''
    class Meta:
        model = Intervention
        exclude = []
        labels = {
            # the quoted text in standard annotator.js parlance is the anchor
            # text for our annotation/marginalia
            # 'tags': 'Annotation type',
            'quote': 'Anchor text',
            # 'author': 'Annotator',
            'uri': 'URI'
        }
        widgets = {
            # 'author': autocomplete.ModelSelect2(
            #     url='people:autocomplete',
            #     attrs={'data-placeholder': 'Start typing name to search...'}),
            'canvas': CanvasLinkWidget(
                url='djiffy:canvas-autocomplete',
                attrs={'data-placeholder': 'Start typing canvas name or uri to search...'}),

        }
        fields = ('canvas', 'intervention_type', 'text', 'text_language',
            'quote', 'quote_language',
            'tags', 'user', 'extra_data', 'uri')

        # fields = ('canvas', 'text', 'tags', 'text_translation', 'languages',
        #           'subjects', 'author', 'quote', 'anchor_translation',
        #           'anchor_languages', 'user', 'extra_data', 'uri')

class InterventionAdmin(AnnotationAdmin):
    form = InterventionAdminForm
    filter_horizontal = ('tags', )
    list_display = ('admin_thumbnail', 'intervention_type', 'text_preview',
        'canvas')
    # NOTE: 'quote' == anchor text, and should be editable
    readonly_fields = ('uri', 'extra_data')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'applies_to')
    list_filter = ('applies_to', )
    fields = ('name', 'applies_to', 'notes')


admin.site.unregister(Intervention)
admin.site.register(Intervention, InterventionAdmin)
admin.site.register(Tag, TagAdmin)