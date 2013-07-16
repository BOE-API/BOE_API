
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
       print 'Probando mongo'



r_count = redis.StrictRedis(host='23.23.215.173', port=6379, db=0)
r = redis.StrictRedis(host='50.17.220.245', port=6379, db=0)


count = Documento.objects.count()
print count
c = int(r_count.get('xmlDB'))
while c < count:
    r_count.set('xmlDB', c + 100)
    for doc in Documento.objects.exclude(url_xml = None).values('url_xml')[c:c+100]:
        r.lpush('BOE', doc['url_xml'])
        print doc['url_xml']
    c = int(r_count.get('xmlDB'))

