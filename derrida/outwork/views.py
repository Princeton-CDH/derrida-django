from django.views.generic import ListView

from derrida.outwork.models import Outwork


class OutworkListView(ListView):
    model = Outwork
    paginate_by = 16

    def get_queryset(self):
        # restrict to published articles
        return Outwork.objects.published(for_user=self.request.user)



