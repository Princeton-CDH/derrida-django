from django import template
from django.utils.timezone import now
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.simple_tag(takes_context=True)
def querystring_replace(context, **kwargs):
    '''Template tag to simplify retaining querystring parameters
    when paging through search results with active filters.
    Example use:

        <a href="?{% querystring_replace page=paginator.next_page_number %}">
    '''
    # inspired by https://stackoverflow.com/questions/2047622/how-to-paginate-django-with-other-get-variables

    # get a mutable copy of the current request
    querystring = context['request'].GET.copy()
    # update with any parameters passed in
    # NOTE: needs to *set* fields rather than using update,
    # because QueryDict update appends to field rather than replacing
    for key, val in kwargs.items():
        querystring[key] = val
    # return urlencoded query string
    return querystring.urlencode()


@register.filter(is_safe=True)
@stringfilter
def format_citation(text, sw_version):
    '''Simple string filter for "how to cite" page to automatically
    add current software version from the context and current date.'''
    return text.replace('[SW_VERSION]', sw_version) \
        .replace('[DATE]', now().strftime('%d %B %Y'))
