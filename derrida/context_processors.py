from django.conf import settings

from derrida.books.forms import SearchForm

def template_settings(request):
    '''Template context processor: add selected setting to context
    so it can be used on any page .'''

    context_extras = {
        'SHOW_TEST_WARNING': getattr(settings, 'SHOW_TEST_WARNING', False),
        'search_form': SearchForm(request.GET)
    }
    return context_extras