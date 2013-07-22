from haystack import indexes
from boe_analisis.models import Documento
from boe_analisis.models import *


class JobIndex(indexes.SearchIndex, indexes.Indexable):
    identificador = indexes.CharField(model_attr='identificador', null=True)
    text = indexes.CharField(document=True, use_template=True, model_attr='texto')
    titulo = indexes.CharField(model_attr='titulo', null=True)
    fecha_publicacion = indexes.DateField(model_attr='fecha_publicacion', null=True)
    # departamento = indexes.CharField(model_attr='departamento__titulo', null=True)
    # materias = indexes.CharField(model_attr='materias__titulo', null=True)

    def get_model(self):
        return Documento

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(titulo=None)

import datetime

# # All Fields
# class AllNoteIndex(indexes.ModelSearchIndex, indexes.Indexable):
#     class Meta:
#         model = Documento
