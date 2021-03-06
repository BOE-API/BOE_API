__author__ = 'Carlos'
import requests
from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from django.db import models
from boe_analisis.models import Documento
from django.db import connection
import re
import datetime
from processDocument import  ProcessDocument
from lxml import etree
from pattern.web import URL

cursor = connection.cursor()
cursor.execute("SELECT max(fecha_publicacion) from boe_analisis_documento")
val = cursor.fetchone()
ultima_fecha = val[0]
if not ultima_fecha:
    ultima_fecha = datetime.date(year=1960, month=1, day=1)

hoy = datetime.date.today() + datetime.timedelta(days=1)
url = "http://www.boe.es/boe/dias/{0}/{1}/{2}/"
url_boe = "http://www.boe.es/diario_boe/xml.php?id={0}"
cursor.close()


class Command(BaseCommand):

    def handle(self, *args, **options):
        print 'Fetching data...'

        if len(args) > 0:
            year = int(args[0])
            month = int(args[1]) if len(args) > 1 else 1
            day = int(args[2]) if len(args) > 2 else 1

            if year < 0 \
                or (month is not None and month not in range(1,12))\
                or (day is not None and day not in range(1, 30)):
                raise AttributeError
            global ultima_fecha


            ultima_fecha = datetime.date(year=year, month=month, day=day)



        for d in daterange(ultima_fecha, hoy):
            print d
            url_day = getURLDay(d)
            print url_day
            req = requests.get(url_day)
            html = BeautifulSoup(req.text)
            link = html.find(href=re.compile("xml"))
            if link:
                url_sum =  'http://www.boe.es' + link.get('href')
                all_docs = []
                procesarSumario(url_sum, all_docs)
                for doc in all_docs:
                    print doc
                    try:
                        d = ProcessDocument(doc)
                        d.saveDoc()
                    except Exception, e:
                        print "fallo " + doc



def daterange(start, stop, step_days=1):
    current = start
    step = datetime.timedelta(step_days)
    if step_days > 0:
        while current < stop:
            yield current
            current += step
    elif step_days < 0:
        while current > stop:
            yield current
            current += step
    else:
        raise ValueError("daterange() step_days argument must not be zero")





def getURLDay(d):

    mes = "%0*d" % (2, d.month)
    dia = "%0*d" % (2, d.day)
    url_day = url.format(d.year, mes, dia)
    return  url_day





def procesarSumario(url_sumario, allDocs):

    url_sumario = url_sumario
    print url_sumario
    content = URL(url_sumario).download()
    xml = etree.XML(content)
    ids = etree.XPath("//item/@id")
    for id in ids(xml):
        url_doc = url_boe.format(id)
        allDocs.append(url_doc)





