# Create your views here.
from django.template import RequestContext
from django.shortcuts import render,render_to_response, redirect
from django.shortcuts import get_object_or_404
from boe_analisis.models import Documento, Materia, Diario
from django.http import HttpResponse
import json

from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import *
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.http import Http404



def home(request):

    documents = Documento.objects.exclude(titulo = None).filter(diario__codigo='BORME')
    paginator = Paginator(documents, 25)
    print paginator.count
    page = request.GET.get('page')
    try:
        lista_docs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        lista_docs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        lista_docs = paginator.page(paginator.num_pages)
    context = {'lista_docs': lista_docs}
    return render_to_response('boe_analisis/index.html', context)


def individual(request, identificador):

    doc = Documento.objects.get(identificador = identificador)
    context = {'doc': doc}
    return render(request, 'boe_analisis/individual.html', context)



def listado_materias(request):
    doc = Materia.objects.all()
    paginator = Paginator(doc, 100)
    page = request.GET.get('page')
    try:
        lista_docs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        lista_docs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        lista_docs = paginator.page(paginator.num_pages)
    context = {'lista_docs': lista_docs}
    return render_to_response('boe_analisis/listado_otros.html', context)




def materias(request, materia):

    mat = Documento.objects.filter(materias__codigo = materia)
    # gob_pp = ['2000','2002', '2003', '2004', '2011', '2012', '2013']
    # gob_psoe = ['2004', '2005', '2006', '2007', '2008','2009','2010','2011']
    # gobs = cache.get('gobs')
    # if not cache.get('gobs'):
    #     gobs = {
    #         'gob_pp' : gob_pp,
    #         'gob_psoe': gob_psoe
    #     }
    # cache.add('gobs', gobs)

    paginator = Paginator(mat, 25)
    page = request.GET.get('page')
    try:
        lista_docs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        lista_docs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        lista_docs = paginator.page(paginator.num_pages)
    context = {'lista_docs': lista_docs}
    return render_to_response('boe_analisis/index.html', context)


def years(request, materia=None):
    cursor = connection.cursor()
    if materia:
        print 'pasa por materia'
        cursor.execute('SELECT distinct(extract(year from fecha_publicacion)) as year_select '
                      ' from boe_analisis_documento doc, boe_analisis_documento_materias mat '
                        'where fecha_publicacion IS NOT NULL and '
                        'doc.id = mat.documento_id and mat.materia_id = %s '
                       'order by  year_select', [materia])


    else:
        print 'pasa por el else'
        cursor.execute('SELECT distinct(extract(year from fecha_publicacion)) as year_select '
                       'from boe_analisis_documento  where fecha_publicacion'
                       ' IS NOT NULL order by  year_select;')
    years = []

    for year in cursor.fetchall():
        # print int(year[0])
        years.append(int(year[0]))
    if len(years) == 0:
        raise Http404

    return HttpResponse(json.dumps(years), content_type="application/json")


def graficos(request):
    count = Documento.objects.filter(fecha_disposicion__gt = '1996-05-01', fecha_disposicion__lt='2004-03-12').count()

    return HttpResponse(count)



