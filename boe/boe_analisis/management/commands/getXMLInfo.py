
from django.db import models
from pymongo import MongoClient
from django.core.management.base import BaseCommand, CommandError
from boe_analisis.models import Diario, Documento, Departamento, Rango, Origen_legislativo
from boe_analisis.models import Estado_consolidacion, Nota, Materia, Alerta, Palabra, Referencia
import os
import sys
from lxml import etree, objectify

from pattern.web import URL

class Command(BaseCommand):

    def handle(self, *args, **options):
       print 'Probando mongo'


for doc in Documento.objects.all():
    print doc
    url = doc.url_xml
    if (url):
        xml = URL(url).download()
        root = etree.XML(xml)
        refAnteriores = []
        refPosteriores = []
        ref = etree.XPath("//referencias")
        ant = etree.XPath("//anterior")
        post = etree.XPath("//posterior")
        for an in ant(root):
            anterior = objectify.fromstring(etree.tostring(an))
            referencia = anterior.get('referencia')
            doc_ref = Documento(identificador=referencia)
            doc_ref.save()
            palabra_codigo = anterior.palabra.get('codigo')
            palabra_texto = anterior.palabra.text
            texto = anterior.texto.text
            palabra = Palabra(codigo = palabra_codigo, titulo=palabra_texto)
            palabra.save()
            ref = Referencia(referencia=doc_ref, palabra=palabra, texto=texto)
            ref.save()
            refAnteriores.append(ref)

        for an in post(root):
            anterior = objectify.fromstring(etree.tostring(an))
            referencia = anterior.get('referencia')
            doc_ref = Documento(identificador=referencia)
            doc_ref.save()
            palabra_codigo = anterior.palabra.get('codigo')
            palabra_texto = anterior.palabra.text
            texto = anterior.texto.text
            palabra = Palabra(codigo = palabra_codigo, titulo=palabra_texto)
            palabra.save()
            ref = Referencia(referencia=doc_ref, palabra=palabra, texto=texto)
            ref.save()
            refPosteriores.append(ref)

        doc.referencias_anteriores = refAnteriores
        doc.referencias_posteriores = refPosteriores
        doc.save()