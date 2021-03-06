from django.views.generic import ListView
from haystack.inputs import Clean, Raw
from haystack.query import SearchQuerySet

from derrida.outwork.models import Outwork


class OutworkListView(ListView):
    model = Outwork
    template_name = 'outwork/outwork_list.html'
    paginate_by = 16

    def get_queryset(self):
        # restrict to published articles
        sqs = SearchQuerySet().models(self.model).filter(published=Raw(True))
        if self.request.GET.get('query', None):
            sqs = sqs.filter(content=Clean(self.request.GET['query']))
        # default sort ?

        return sqs
