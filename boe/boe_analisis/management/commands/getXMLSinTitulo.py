
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
from django.db import transaction
import atexit
from django.db import IntegrityError, transaction

class Command(BaseCommand):

    def handle(self, *args, **options):
       print 'Probando mongo'


url_s_pattern = "http://www.boe.es/diario_boe/xml.php?id=BOE-S-{0}-{1}"
url_a_pattern =  "http://www.boe.es/diario_boe/xml.php?id={0}"
url_a_html_pattern = "http://www.boe.es/diario_boe/txt.php?id={0}"

r_count = redis.StrictRedis(host='crawler1', port=6379, db=0)
r = redis.StrictRedis(host='redis', port=6379, db=0)


if (len(sys.argv) >= 3):
    rango =  sys.argv[2]

else:
    print 'manda un argumento'
    sys.exit()

if len(sys.argv) >=4:
    count = int(sys.argv[3])
else:
    count = int(r_count.get(rango))
max = r.llen(rango)

test_ue = r.lrange(rango, count, count+100)

# print test_ue
f = file('fallos.txt', 'a')

def process(test_ue):

    for url in test_ue:
        print 'OUT ' + url
        try:
            if not Documento.objects.filter(url_xml = url).exclude(Q(titulo = None) |
                                                                   Q(referencias_anteriores=None) |
                                                                   Q(referencias_posteriores=None) |
                                                                   Q(notas=None) |
                                                                   Q(alertas=None) |
                                                                   Q(materias=None) |
                                                                   Q(texto=None)).exists():
                print url
                documento = Documento()
                fillDocumentXMLData(url, documento)
                transaction.commit_on_success()

        except Exception, e:
            print e
            print 'FALLO'
            print url
            f.write(url)
            f.(e)


while count < max:
    print count
    test_ue = r.lrange(rango, count, count+100)
    r_count.set(rango, int(count+100))
    # docs = []
    process(test_ue)




    count = int(r_count.get(rango))

    print count





# print count
#
# while int(count) < max:
#     r_count.incr('count_empty', amount=10)
#     for e in test[count:count+10]:
#         url = url_a_pattern.format(e.identificador)
#         print url
#         fillDocumentXMLData(url, e)
#
#     count = int(r_count.get('count_empty'));
#


