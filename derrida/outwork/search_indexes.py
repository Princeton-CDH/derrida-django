# import datetime
from haystack import indexes
from derrida.outwork.models import Outwork

# currently keeping outwork index very simple; no facets, just index
# to allow full-text serach

class OutworkIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, stored=False)
    title = indexes.CharField(model_attr='title')
    #: author name; firstname lastname for display
    author = indexes.CharField(model_attr='author__firstname_last', null=True)
    orig_pubdate = indexes.DateField(model_attr='orig_pubdate', null=True)
    description = indexes.CharField(model_attr='description')
    slug = indexes.CharField(model_attr='slug')
    published = indexes.BooleanField(model_attr='is_published')

    def get_model(self):
        return Outwork

