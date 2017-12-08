from django.conf.urls import url, include
from django.contrib.admin.views.decorators import staff_member_required

from derrida.outwork import views

urlpatterns = [
    url(r'^$', views.OutworkListView.as_view(), name='list'),
    # individual outwork pages handled by mezzanine
]
