
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
import timeit
class Command(BaseCommand):

    def handle(self, *args, **options):
       print 'Probando mongo'

def query():
    for d in Documento.objects.raw('SELECT titulo, identificador from boe_analisis_documento order by titulo asc limit 25 offset 1000000'):
        print d

print timeit.timeit(query, number=1)