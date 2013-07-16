
from django.db import models
from pymongo import MongoClient
from django.core.management.base import BaseCommand, CommandError
from boe_analisis.models import Diario, Documento, Departamento, Rango, Origen_legislativo
from boe_analisis.models import Estado_consolidacion, Nota, Materia, Alerta, Palabra, Referencia
import os
import sys
from django.db.models import Q
import redis
from lxml import etree, objectify

from pattern.web import URL

class Command(BaseCommand):

    def handle(self, *args, **options):
       print 'Probando mongo'


r = redis.StrictRedis(host='23.23.215.173', port=6379, db=0)

test = Documento.objects.filter(titulo=None).exclude(Q(identificador__istartswith='--') | Q(identificador__istartswith='B-B'))

#
for e in test[:1000]:
    print e

