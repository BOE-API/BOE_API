
from django.db import models
from pymongo import MongoClient
from django.core.management.base import BaseCommand, CommandError
from boe_analisis.models import Diario, Documento, Departamento, Rango, Origen_legislativo
from boe_analisis.models import Estado_consolidacion, Nota, Materia, Alerta, Palabra, Referencia
import os
import sys
from django.db.models import Q
import redis
import re
from datetime import datetime
from lxml import etree, objectify

from pattern.web import URL

class Command(BaseCommand):

    def handle(self, *args, **options):
       fillRedis()
       print 'Probando mongo'


url_s_pattern = "http://www.boe.es/diario_boe/xml.php?id=BOE-S-{0}-{1}"
url_a_pattern =  "http://www.boe.es/diario_boe/xml.php?id={0}"
url_a_html_pattern = "http://www.boe.es/diario_boe/txt.php?id={0}"

r_count = redis.StrictRedis(host='23.23.215.173', port=6379, db=0)
r = redis.StrictRedis(host='REDIS', port=6379, db=0)
max = 2;
count = 0;

regex = re.compile("(\d{4})(\d{2})(\d{2})")
def textToDate(texto):
    global regex
    print texto
    if texto is not None:
        match = re.match(regex, texto)
        if match != None:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            d = datetime(year,month, day)
            return d
    return None

def SiNoToBool(character):
    return character == 'S'



def fillDocumentXMLData(url_xml_Input, documento):
    """

    :param url_xml_Input:
    :param documento:
    """
    print url_xml_Input
    url_xml = URL(url_xml_Input)
    xmlDOC = url_xml.download()

    rootXML = objectify.fromstring(xmlDOC)


    metadatos = rootXML.metadatos
    if hasattr(metadatos, 'identificador'):
        documento.identificador = metadatos.identificador.text

        documento.url_xml = url_a_pattern.format(metadatos.identificador.text)
        documento.url_htm = url_a_html_pattern.format(metadatos.identificador.text)
    else:
        raise Exception
    if hasattr(metadatos, 'titulo'):
        documento.titulo = metadatos.titulo.text
    if hasattr(metadatos, 'diario'):


        if metadatos.diario.get('codigo'):
            codigo = metadatos.diario.get('codigo')
            titulo = metadatos.diario.text
            diario = Diario.objects.get_or_create(codigo=codigo, titulo=titulo)[0]
            documento.diario = diario
    if hasattr(metadatos, 'diario_numero'):
        documento.diario_numero = metadatos.diario_numero.text
    if hasattr(metadatos, 'seccion'):
        documento.seccion = metadatos.seccion.text
    if hasattr(metadatos, 'subseccion'):
        documento.subseccion = metadatos.subseccion.text
    if hasattr(metadatos, 'departamento'):

        if metadatos.departamento.get('codigo'):
            codigo = metadatos.departamento.get('codigo')
            titulo = metadatos.departamento.text
            dept = Departamento.objects.get_or_create(codigo=codigo, titulo=titulo)[0]
            documento.departamento = dept
    if hasattr(metadatos, 'rango'):

        codigo = int(metadatos.rango.get('codigo'))
        titulo = metadatos.rango.text
        rango = Rango.objects.get_or_create(codigo=codigo, titulo=titulo)[0]
        documento.rango = rango
    if hasattr(metadatos, 'numero_oficial'):
        documento.numero_oficial = metadatos.numero_oficial.text
    if hasattr(metadatos, 'fecha_disposicion'):
        documento.fecha_disposicion = textToDate(metadatos.fecha_disposicion.text)
    if hasattr(metadatos, 'fecha_publicacion'):
        documento.fecha_publicacion = textToDate(metadatos.fecha_publicacion.text)
        print textToDate(metadatos.fecha_publicacion.text)
    if hasattr(metadatos, 'fecha_vigencia'):
        documento.fecha_vigencia = textToDate(metadatos.fecha_vigencia.text)
    if hasattr(metadatos, 'fecha_derogacion'):
        documento.fecha_derogacion = textToDate(metadatos.fecha_derogacion.text)
    if hasattr(metadatos, 'letra_imagen'):
        documento.letra_imagen = metadatos.letra_imagen.text
    if hasattr(metadatos, 'pagina_inicial'):
        documento.pagina_inicial = int(metadatos.pagina_inicial.text)
    if hasattr(metadatos, 'pagina_final'):
        documento.pagina_final = int(metadatos.pagina_final.text)
    if hasattr(metadatos, 'suplemento_pagina_inicial'):
        documento.suplemento_pagina_inicial = metadatos.suplemento_pagina_inicial.text
    if hasattr(metadatos, 'suplemento_pagina_final'):
        documento.suplemento_pagina_final = metadatos.suplemento_pagina_final.text
    if hasattr(metadatos, 'estatus_legislativo'):
        documento.estatus_legislativo = metadatos.estatus_legislativo.text
    if hasattr(metadatos, 'origen_legislativo'):

        codigo = metadatos.origen_legislativo.get('codigo')
        titulo = metadatos.origen_legislativo.text
        origen = Origen_legislativo.objects.get_or_create(codigo=codigo, titulo=titulo)[0]
        documento.origen_legislativo = origen
    if hasattr(metadatos, 'estado_consolidacion'):
        est =  metadatos.estado_consolidacion
        estado_codigo = est.get('codigo')
        estado_texto = est.text
        if estado_codigo != '' and estado_texto:
            estado = Estado_consolidacion.objects.get_or_create(codigo=int(estado_codigo), titulo=estado_texto)[0]

            documento.estado_consolidacion = estado
    if hasattr(metadatos, 'judicialmente_anulada'):
        documento.judicialmente_anulada = SiNoToBool(metadatos.judicialmente_anulada.text)
    if hasattr(metadatos, 'vigencia_agotada'):
        documento.vigencia_agotada = SiNoToBool(metadatos.vigencia_agotada.text)
    if hasattr(metadatos, 'estatus_derogacion'):
        documento.estatus_derogacion = SiNoToBool(metadatos.estatus_derogacion.text)

    if hasattr(metadatos, 'url_epub'):
        documento.url_epub = metadatos.url_epub.text
    if hasattr(metadatos, 'url_pdf'):
        documento.url_pdf = metadatos.url_pdf.text
    if hasattr(metadatos, 'url_pdf_catalan'):
        documento.url_pdf_catalan = metadatos.url_pdf_catalan.text
    if hasattr(metadatos, 'url_pdf_euskera'):
        documento.url_pdf_euskera = metadatos.url_pdf_euskera.text
    if hasattr(metadatos, 'url_pdf_gallego'):
        documento.url_pdf_gallego = metadatos.url_pdf_gallego.text
    if hasattr(metadatos, 'url_pdf_valenciano'):
        documento.url_pdf_valenciano = metadatos.url_pdf_valenciano.text
    documento.save()
    notas = []
    if hasattr(rootXML.analisis, 'notas'):
        if hasattr(rootXML.analisis.notas, 'nota'):

            for nota in rootXML.analisis.notas.nota:
                notaCodigo = nota.get('codigo')
                notaTitulo = nota.text
                n = Nota.objects.get_or_create(codigo=notaCodigo, titulo=notaTitulo)[0]
                notas.append(n)
                print n.codigo



    alertas = []
    if hasattr(rootXML.analisis, 'materias'):
        if hasattr(rootXML.analisis.materias, 'materia'):
            materias = []
            for materia in rootXML.analisis.materias.materia:
                codigo = materia.get('codigo')
                titulo = materia.text
                mat = Materia.objects.get_or_create(codigo=codigo, titulo=titulo)[0]
                materias.append(mat)
            documento.materias = materias
    if hasattr(rootXML.analisis, 'alertas'):
        if hasattr(rootXML.analisis.alertas, 'alerta'):
            for alerta in rootXML.analisis.alertas.alerta:
                codigo = alerta.get('codigo')
                titulo = alerta.text
                a = Alerta.objects.get_or_create(codigo=codigo, titulo=titulo)[0]

                alertas.append(a)


    if hasattr(rootXML.analisis, 'anteriores'):
        if hasattr(rootXML.analisis.referencias.anteriores, 'anterior'):
            refAnteriores = []
            for anterior in rootXML.analisis.referencias.anteriores.anterior:

                referencia = anterior.get('referencia')
                doc_ref = Documento.objects.get_or_create(identificador=referencia)

                palabra_codigo = anterior.palabra.get('codigo')
                palabra_texto = anterior.palabra.text
                texto = anterior.texto.text

                palabra = Palabra.objects.get_or_create(codigo = palabra_codigo, titulo=palabra_texto)
                ref = Referencia.objects.get_or_create(referencia=doc_ref, palabra=palabra, texto=texto)
                refAnteriores.append(ref)
            documento.referencias_anteriores = refAnteriores
    if hasattr(rootXML.analisis, 'posteriores'):
        if hasattr(rootXML.analisis.referencias.posteriores, 'posterior'):
            refPosteriores = []
            for anterior in rootXML.analisis.referencias.posteriores.posterior:
                referencia = anterior.get('referencia')
                doc_ref = Documento.objects.get_or_create(identificador=referencia)
                palabra_codigo = anterior.palabra.get('codigo')
                palabra_texto = anterior.palabra.text
                texto = anterior.texto.text
                palabra = Palabra.objects.get_or_create(codigo = palabra_codigo, titulo=palabra_texto)
                ref = Referencia.objects.get_or_create(referencia=doc_ref, palabra=palabra, texto=texto)
                refPosteriores.append(ref)
            documento.referencias_posteriores = refPosteriores
    if hasattr(rootXML, 'texto'):
        textoString = etree.tostring(rootXML.texto, pretty_print=True)
        documento.texto = textoString
    if notas:
        documento.notas = notas
    if alertas:
        documento.alertas = alertas

    documento.save()
    return documento


def fillRedis():
    pattern = '*'

    while int(anyo) <= 2013:
        search = pattern.format(r_count.get('anyo'))
        r_count.incr('anyo')
        print search
        for k in r.keys(search):
            documento = Documento()
            print k
            try:
                fillDocumentXMLData(k, documento)
                r.delete(k)
            except:
                pass

        anyo = r_count.get('anyo')


# for k in r.keys('*-18??-*'):
#             documento = Documento()
#             print k
#             fillDocumentXMLData(k, documento)
#             r.delete(k)
# #
# while count < max:
#     for e in test[count:count+10]:
#         url = url_a_pattern.format(e.identificador)
#         print url
#         fillDocumentXMLData(url, e)



