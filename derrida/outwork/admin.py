from copy import deepcopy

from dal import autocomplete
from django.contrib import admin
from mezzanine.pages.models import RichTextPage
from django.contrib import admin
from django.utils import timezone
from mezzanine.pages.admin import PageAdmin, PageAdminForm

from derrida.outwork.models import Outwork


# customize page admin fieldset for outwork
# move description from metadata to main, since we are using it as excerpt
# remove in menus and login required
outwork_fieldsets = deepcopy(PageAdmin.fieldsets)
# outwork_fieldsets[0][1]['fields'].insert(3, 'content')
# outwork_fieldsets[0][1]['fields'].insert(3, ('description', 'gen_description'))
outwork_fieldsets[0][1]['fields'].remove('in_menus')
outwork_fieldsets[0][1]['fields'].extend(['author', 'orig_pubdate',
    ('description', 'gen_description'), 'content'])
outwork_fieldsets[0][1]['fields'].remove('login_required')
outwork_fieldsets[1][1]['fields'].remove(('description', 'gen_description'))
outwork_fieldsets[1][1]['fields'].remove(('in_sitemap'))
# use grappelli collapse logic, default open
outwork_fieldsets[1][1]['classes'] = ('grp-collapse grp-open',)


class OutworkAdminForm(PageAdminForm):
    help_text = {
        'description': '''Excerpt for display at the top of the page and
            in list view; also used as description in page metadata and
            for link previews.''',
        'slug': ''' Outwork and site publication year will automatically be added.
        Should not be changed after an item is published.''',
        'keywords': '''Optional list of comma-separated keywords for inclusion
            in page metadata''',
    }
    class Meta:
        widgets = {
            'author': autocomplete.ModelSelect2(
                url='people:person-autocomplete',
                attrs={'data-placeholder': 'Start typing a name to search...'}
            )
        }

    def __init__(self, *args, **kwargs):
        super(OutworkAdminForm, self).__init__(*args, **kwargs)
        # expand help text
        for field, help_text in self.help_text.items():
            self.fields[field].help_text += help_text
        self.fields['description'].label = 'Excerpt'
        self.fields['gen_description'].initial = False


class OutworkAdmin(PageAdmin):
    form = OutworkAdminForm
    fieldsets = outwork_fieldsets


page_fieldsets = deepcopy(PageAdmin.fieldsets)
# make sure content is included
page_fieldsets[0][1]['fields'].append('content')
# use grappelli collapse logic, default open
page_fieldsets[1][1]['classes'] = ('grp-collapse grp-open',)

class LocalPageAdmin(PageAdmin):
    fieldsets = page_fieldsets


admin.site.register(Outwork, OutworkAdmin)
admin.site.unregister(RichTextPage)
admin.site.register(RichTextPage, LocalPageAdmin)
