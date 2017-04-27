from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from derrida.books.views import PublisherAutocomplete


urlpatterns = [
    url(r'^autocomplete/publisher/$', staff_member_required(PublisherAutocomplete.as_view()),
        name='publisher-autocomplete'),
]
