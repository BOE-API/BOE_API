
from django.db import models
from pymongo import MongoClient
from django.core.management.base import BaseCommand, CommandError
from boe_analisis.models import Diario, Documento, Departamento, Rango, Origen_legislativo
from boe_analisis.models import Estado_consolidacion, Nota, Materia, Alerta, Palabra, Referencia
import os
import sys
import redis
class Command(BaseCommand):

    def handle(self, *args, **options):
       print 'Probando mongo'

client = MongoClient('mongodb://charlisim:tesa2,mujir@ds035118-a0.mongolab.com:35118,ds035118-spare.mongolab.com:35118/boe')
db = client['boe']
docs = db['documento']
global_diarios = []
r = redis.StrictRedis(host='23.23.215.173', port=6379, db=0)
print r.get('counter')
c = int(r.get('counter'))
max = docs.count()
while c < max:

    r.set('counter', c + 100)

    for doc in docs.find().skip(c).limit(100):
        print doc

        id = doc['_id']
        titulo = doc['titulo']
        diario = doc['diario']
        seccion = doc['seccion']
        rango = doc['rango'] if 'rango' in doc else None
        subseccion = doc['subseccion'] if 'subseccion' in doc else None
        diario_numero = doc['diario_numero'] if 'diario_numero' in doc else None
        dept =  doc['departamento'] if 'departamento' in doc else None
        num_oficial = doc['numero_oficial'] if 'numero_oficial' in doc else None
        fecha_disposicion = doc['fecha_disposicion'] if 'fecha_disposicion' in doc else None
        fecha_publicacion = doc['fecha_publicacion'] if 'fecha_publicacion' in doc else None
        fecha_vigencia = doc['fecha_vigencia'] if 'fecha_vigencia' in doc else None
        fecha_derogacion = doc['fecha_derogacion'] if 'fecha_derogacion' in doc else None
        url_epub = doc['url_epub'] if 'url_epub' in doc else None
        url_xml = doc['url_xml'] if 'url_xml' in doc else None
        print url_xml
        url_htm = doc['url_htm'] if 'url_htm' in doc else None
        url_pdf = doc['url_pdf'] if 'url_pdf' in doc else None
        url_pdf_catalan = doc['url_pdf_catalan'] if 'url_pdf_catalan' in doc else None
        url_pdf_euskera = doc['url_pdf_euskera'] if 'url_pdf_euskera' in doc else None
        url_pdf_gallego = doc['url_pdf_gallego'] if 'url_pdf_gallego' in doc else None
        url_pdf_valenciano = doc['url_pdf_valenciano'] if 'url_pdf_valenciano' in doc else None
        notas = doc['notas'] if 'notas' in doc else None
        materias = doc['materias'] if 'materias' in doc else None
        alertas = doc['alertas'] if 'alertas' in doc else None
        referencias_anteriores = doc['referencias_anteriores'] if 'referencias_anteriores' in doc else None
        referencias_posteriores = doc['referencias_posteriores'] if 'referencias_posteriores' in doc else None
        texto = doc['texto_html'] if 'texto_html' in doc else None



        Odiario = Diario(codigo=diario['codigo'], titulo=diario['titulo'])
        Odiario.save()
        ORango = None
        if rango:
            ORango = Rango(codigo=rango['codigo'], titulo=rango['titulo'])
            # print ORango.titulo
            ORango.save()
        ODepartamento = None
        if dept:
            ODepartamento = Departamento(codigo=dept['codigo'], titulo=dept['titulo'])
            # print ODepartamento
            ODepartamento.save()

        ONotas = []
        if notas:
            for nota in notas:

                n = Nota(codigo=nota['codigo'], titulo=nota['titulo'])
                # print n.titulo
                # print n.codigo
                try:
                    n.save()
                    ONotas.append(n)
                except:
                    try:
                        n = Nota.objects.get(codigo=nota['codigo'], titulo=nota['titulo'])
                        ONotas.append(n)
                    except:
                        pass
        OMaterias = []
        if materias:
            for materia in materias:
                m = Materia(codigo=materia['codigo'], titulo=materia['titulo'])
                # print m.titulo
                m.save()
                OMaterias.append(m)
        OAlertas = []
        if alertas:
            for alerta in alertas:
                a = Alerta(codigo=alerta['codigo'], titulo=alerta['titulo'])
                a.save()
                # print a.titulo
                OAlertas.append(a)

        ORef_Anteriores = []
        if referencias_anteriores:
            for r_ant in referencias_anteriores:
                ra = Referencia(codigo=r_ant['codigo'], titulo=r_ant['titulo'])
                ra.save()
                # print ra.titulo
                ORef_Anteriores.append(ra)

        ORef_Posteriores = []
        if referencias_posteriores:
            for r_ant in referencias_posteriores:
                ra = Referencia(codigo=r_ant['codigo'], titulo=r_ant['titulo'])
                ra.save()
                # print ra.titulo
                ORef_Posteriores.append(ra)

        documento = Documento()
        documento.identificador = id
        documento.titulo = titulo
        documento.save()
        documento.diario = Odiario
        documento.diario_numero = diario_numero
        documento.seccion = seccion
        documento.subseccion = subseccion
        documento.rango = ORango
        documento.Departamento = ODepartamento
        documento.numero_oficial = num_oficial
        documento.fecha_disposicion = fecha_disposicion
        documento.fecha_publicacion = fecha_publicacion
        documento.fecha_vigencia = fecha_vigencia
        documento.fecha_derogacion = fecha_derogacion
        documento.url_epub = url_epub
        documento.url_xml = url_xml
        documento.url_htm = url_htm
        documento.url_pdf = url_pdf
        documento.url_pdf_catalan = url_pdf_catalan
        documento.url_pdf_euskera = url_pdf_euskera
        documento.url_pdf_gallego = url_pdf_gallego
        documento.url_pdf_valenciano = url_pdf_valenciano
        documento.notas = ONotas
        documento.materias = OMaterias
        documento.alertas = OAlertas
        documento.referencias_anteriores = ORef_Anteriores
        documento.referencias_posteriores = ORef_Posteriores
        documento.texto = texto

        documento.save()

    c = int(r.get('counter'))