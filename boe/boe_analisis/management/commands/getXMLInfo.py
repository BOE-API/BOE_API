
from django.db import models
from pymongo import MongoClient
from django.core.management.base import BaseCommand, CommandError
from boe_analisis.models import Diario, Documento, Departamento, Rango, Origen_legislativo
from boe_analisis.models import Estado_consolidacion, Nota, Materia, Alerta, Palabra, Referencia
import os
import sys
import redis
from lxml import etree, objectify

from pattern.web import URL

class Command(BaseCommand):

    def handle(self, *args, **options):
       print 'Probando mongo'

r = redis.StrictRedis(host='23.23.215.173', port=6379, db=0)
f = file('xml_failed.txt', 'w+')
c = int(r.get('counter_xml'))
max = Documento.objects.count()
while c < max:
    print c
    r.set('counter_xml', c + 100)
    for doc in Documento.objects.all()[c:c+100]:
        print doc.identificador
        url = doc.url_xml
        if (url):
            xml = URL(url).download()
            root = etree.XML(xml)
            refAnteriores = []
            refPosteriores = []
            ref = etree.XPath("//referencias")
            origen = etree.XPath("//origen_legislativo")
            estado = etree.XPath("//estado_consolidacion")
            ant = etree.XPath("//anterior")
            post = etree.XPath("//posterior")
            try:

                for an in ant(root):

                    anterior = objectify.fromstring(etree.tostring(an))
                    referencia = anterior.get('referencia')
                    doc_ref = Documento(identificador=referencia)
                    doc_ref.save()
                    palabra_codigo = anterior.palabra.get('codigo')
                    palabra_texto = anterior.palabra.text
                    texto = anterior.texto.text
                    print doc_ref.identificador
                    palabra = Palabra(codigo = palabra_codigo, titulo=palabra_texto)
                    palabra.save()
                    ref = Referencia(referencia=doc_ref, palabra=palabra, texto=texto)
                    try:
                        ref.save()
                    except:
                        try:
                            ref = Referencia.objects.get(referencia=doc_ref, palabra=palabra)
                        except:
                            pass

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
                    try:
                        ref.save()
                    except:
                        try:
                            ref = Referencia.objects.get(referencia=doc_ref, palabra=palabra)
                        except:
                            pass
                    refPosteriores.append(ref)

                for ori in origen(root):
                    origen_codigo = ori.get('codigo')
                    origen_texto = ori.text
                    orig = Origen_legislativo(codigo=int(origen_codigo), titulo=origen_texto)
                    orig.save()
                    doc.origen_legislativo = orig
                for est in estado(root):
                    estado_codigo = est.get('codigo')
                    if (estado_codigo != ''):
                        estado_texto = est.text
                        estado = Estado_consolidacion(codigo=int(estado_codigo), titulo=estado_texto)
                        estado.save()

                doc.referencias_anteriores = refAnteriores
                doc.referencias_posteriores = refPosteriores
                doc.save()
            except:
                f.write(doc.identificador)

    c = int(r.get('counter_xml'))