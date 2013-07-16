
from django.db import models
from pymongo import MongoClient
from django.core.management.base import BaseCommand, CommandError
from boe_analisis.models import Diario, Documento, Departamento, Rango, Origen_legislativo
from boe_analisis.models import Estado_consolidacion, Nota, Materia, Alerta, Palabra, Referencia
import os
import sys
from getXMLRedis import fillDocumentXMLData
from django.db.models import Q
import redis
import re
from datetime import datetime
from lxml import etree, objectify

from pattern.web import URL

class Command(BaseCommand):

    def handle(self, *args, **options):
       print 'Probando mongo'


url_s_pattern = "http://www.boe.es/diario_boe/xml.php?id=BOE-S-{0}-{1}"
url_a_pattern =  "http://www.boe.es/diario_boe/xml.php?id={0}"
url_a_html_pattern = "http://www.boe.es/diario_boe/txt.php?id={0}"

r_count = redis.StrictRedis(host='23.23.215.173', port=6379, db=0)
r = redis.StrictRedis(host='50.17.220.245', port=6379, db=0)
max = 100000
count = int(r_count.get('count_empty'));







print count
test = Documento.objects.filter(titulo=None).exclude(
    Q(identificador__istartswith='--') |
    Q(identificador__istartswith='B-B') |
    Q(identificador__istartswith='BOA'))

while int(count) < max:

    for e in test[count:count+10]:
        url = url_a_pattern.format(e.identificador)
        print url
        fillDocumentXMLData(url, e)
        count = int(r.set('count_empty',int(r_count.get('count_empty')) + 10));



