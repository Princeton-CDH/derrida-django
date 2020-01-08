from django.conf.urls import url

from derrida.outwork import views


app_name = 'derrida.outwork'

urlpatterns = [
    url(r'^$', views.OutworkListView.as_view(), name='list'),
    # individual outwork pages handled by mezzanine
]
