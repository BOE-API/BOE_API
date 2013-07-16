from haystack import indexes
from boe_analisis.models import Documento
from boe_analisis.models import *
class JobIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, model_attr='texto')
    titulo = indexes.CharField(model_attr='titulo') 
    def get_model(self):
        return Documento
 
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
