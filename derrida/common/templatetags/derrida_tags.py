from django import template

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
    querystring.update(kwargs)
    # return urlencoded query string
    return querystring.urlencode()


@register.filter()
def format_for_home(context):
    '''Template filter to format richtext from content management
    to the html needed to render the layout of the homepage.
    The main content is to be contained between blocks

        [main] ... [/main]

    The credits content is contained with blocks much like the main block
    with a few additonal expectations - the credit role is expected to be
    wrapped in a strong tag and the name of the person wrapped in an em tag.

        [credits]
            <strong>Title</strong>
            <em>Name</em>
            <em>Name</em>
            ...
        [/credits]

    Example use:

        {{ page.richtextpage.content|richtext_filters|format_for_home|safe }}
    '''

    def getContentForBlock(tag):
        start = "<p>[%s]</p>" % tag
        end = "<p>[/%s]</p>" % tag
        return context[context.index(start):context.index(end)][len(start):]

    mainContent = "<section>%s</section>" % getContentForBlock('main')
    creditContent = "<aside><dl class='credits'>%s</dl></aside>" % \
                    getContentForBlock('credits')\
                    .replace('<strong>', '<dt class="credits__role">')\
                    .replace('</strong>', '</dt>')\
                    .replace('<em>', '<dd class="credits__name">')\
                    .replace('</em>', '</dd>')\
                    .replace('<br>', '')

    return mainContent + creditContent
