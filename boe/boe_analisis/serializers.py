__author__ = 'Carlos'
from boe_analisis.models import Documento, Diario, Materia

from rest_framework import serializers

class DocumentoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Documento
        fields = ('id', 'identificador', 'titulo', 'diario', 'materias', 'texto')

class MateriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Materia
        fields = ('codigo', 'titulo')




class DiarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Diario
        fields = ('codigo', 'titulo')

