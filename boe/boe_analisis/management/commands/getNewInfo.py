__author__ = 'Carlos'
import requests
from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from django.db import models
from boe_analisis.models import Documento
from django.db import connection
import re
import datetime
from getXMLRedis import fillDocumentXMLData
from lxml import etree
from pattern.web import URL
class Command(BaseCommand):

    def handle(self, *args, **options):
       print 'Probando mongo'


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



cursor = connection.cursor()

cursor.execute("SELECT max(fecha_publicacion) from boe_analisis_documento")
val = cursor.fetchone()
ultima_fecha = val[0]
hoy = datetime.date.today()
url = "http://www.boe.es/boe/dias/{0}/{1}/{2}/"
url_boe = "http://www.boe.es/diario_boe/xml.php?id={0}"
cursor.close()
def getURLDay(d):

    mes = "%0*d" % (2, d.month)
    dia = "%0*d" % (2, d.day)
    url_day = url.format(d.year, mes, dia)
    return  url_day





def getSumarios():
    xmlSumarioToProcess = []
    for d in daterange(ultima_fecha, hoy):
        url_day = getURLDay(d)
        # print url_day
        req = requests.get(url_day)
        html = BeautifulSoup(req.text)
        link = html.find(href=re.compile("xml"))
        if link:
            url_sum =  'http://www.boe.es' + link.get('href')
            xmlSumarioToProcess.append(url_sum)
    return xmlSumarioToProcess
all_docs = []
def procesarSumario(url_sumario, allDocs):

    url_sumario = url_sumario
    content = URL(url_sumario).download()
    xml = etree.XML(content)
    ids = etree.XPath("//item/@id")
    for id in ids(xml):
        url_doc = url_boe.format(id)
        allDocs.append(url_doc)


for sumario in getSumarios():
    procesarSumario(sumario, all_docs)

for doc in all_docs:
    docum = Documento()
    print doc
    fillDocumentXMLData(doc, docum)




print len(all_docs)






print val[0]

