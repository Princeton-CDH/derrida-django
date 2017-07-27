from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from derrida.books.views import (
    PublisherAutocomplete, LanguageAutocomplete, InstanceListView
)


urlpatterns = [
    # TODO: come up with cleaner url patterns/names for autocomplete views
    url(r'^publishers/autocomplete/$', staff_member_required(PublisherAutocomplete.as_view()),
        name='publisher-autocomplete'),
    url(r'^languages/autocomplete/$', staff_member_required(LanguageAutocomplete.as_view()),
        name='language-autocomplete'),
    url(r'^$', InstanceListView.as_view(), name='list')

]
