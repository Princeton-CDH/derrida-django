from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from derrida.people.views import PersonAutocomplete


urlpatterns = [
    url(r'^autocomplete/person/$', staff_member_required(PersonAutocomplete.as_view()),
        name='person-autocomplete'),
]
