
from django.db import models
from pymongo import MongoClient
from django.core.management.base import BaseCommand, CommandError
from boe_analisis.models import Diario, Documento, Departamento, Rango, Origen_legislativo
from boe_analisis.models import Estado_consolidacion, Nota, Materia, Alerta, Palabra, Referencia
import os
import sys
import re
import urllib
import redis
import requests
import BeautifulSoup as bs4
from BeautifulSoup import BeautifulSoup
from lxml import etree, objectify

from pattern.web import URL

class Command(BaseCommand):

    def handle(self, *args, **options):
       print 'Probando mongo'

r_count = redis.StrictRedis(host='23.23.215.173', port=6379, db=0)

r = redis.StrictRedis(host='50.17.220.245', port=6379, db=0)
bormce_url_s = 'http://www.boe.es/diario_borme/xml.php?id=BORME-S-{0}-{1}'
bormce_url_xml = 'http://www.boe.es/diario_borme/xml.php?id={0}'

def fillBormce():
    for anyo in range(2001, 2014):
        for dia in range(1, 365):
            url =  bormce_url_s.format(anyo, dia)
            req = requests.get(url)
            bs = BeautifulSoup(req.content)
            for x in bs.findAll('seccion', num='C'):
                for item in x.findAll('item'):
                    url_bormce =  bormce_url_xml.format(item.get('id'))
                    print url_bormce
                    r.lpush('bormce', url_bormce)
def generalFill(params, lista):
    url = 'http://www.boe.es/legislacion/legislacion.php?'
    url_xml = 'http://www.boe.es/diario_boe/xml.php?id={0}'
    url_time = url + params
    cookies = dict(SESSID='l5bvc0pl90qerp0vmsq5rq4bd6',
                   BOElang='es',
                   )


    req = requests.get(url_time, allow_redirects=True, cookies=cookies)
    print url_time
    bs = BeautifulSoup(req.content)
    for enlace in bs.findAll('a'):
        # print enlace
        if enlace.get('href'):
            reg = re.search(".*\?id=(.*)", enlace.get('href'))
            if reg:
                id = reg.group(1)
                url_id =  url_xml.format(id)
                print url_id
                r.lpush(lista, url_id)


def fillUE():
    for times in range(0, 60000, 1000):
        params = urllib.urlencode({
            'accion' : 'Mas',
            'id_busqueda': '4ffd7543ab29b2741e56aa1545f2e85a-{0}-1000'.format(times),

            })
        generalFill(params, 'UE')

def fillComunidades():
    for times in range(0, 10000, 1000):
        params = urllib.urlencode({
            'accion' : 'Mas',
            'id_busqueda': 'f8658daaf3853a711553bb983469fd18-{0}-1000'.format(times),

            })
        generalFill(params, 'CCAA')

def fillEstatal():
    for times in range(0, 183391, 1000):
        params = urllib.urlencode({
            'accion' : 'Mas',
            'id_busqueda': '09aeb0209ecc876d819e3958a60ba9c7-{0}-1000'.format(times),

            })
        generalFill(params, 'BOE')


def fillInDB():
    count = Documento.objects.count()
    print count
    c = int(r_count.get('xmlDB'))
    while c < count:
        r_count.set('xmlDB', c + 100)
        for doc in Documento.objects.exclude(url_xml = None).values('url_xml')[c:c+100]:
            r.lpush('BOE', doc['url_xml'])
            print doc['url_xml']
        c = int(r_count.get('xmlDB'))

if (r_count.get('bormce') == '0'):
    fillBormce()
    r_count.set('bormce', 1)
if (r_count.get('UE') == '0'):
    fillUE()
    r_count.set('bormce', 1)
if (r_count.get('CCAA') == '0'):
    fillComunidades()
    r_count.set('CCAA', 1)
if (r_count.get('DB') == '0'):
    fillEstatal()
    r_count.set('DB', 1)