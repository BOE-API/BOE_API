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


def leyes_meses_legislatura(request, meses=48):
    if int(meses) >= 48:
        meses = 48


    cursor = connection.cursor()
    cursor.execute("SELECT leg.nombre_legislatura, leg.id , leg.presidente, count(*)"
    "from boe_analisis_documento doc, boe_analisis_legislatura leg "
      "where doc.legislatura_id = leg.id "
      "and doc.fecha_disposicion > leg.inicio and doc.fecha_disposicion <= (leg.inicio) + (%s || ' month')::INTERVAL "
      "group by leg.nombre_legislatura, leg.presidente, leg.id order by leg.id;", [int(meses)]
      )
    legislatura_array = []
    legislatura_array.append({'meses': meses})
    for legislatura in cursor.fetchall():
        ley = {

            'codigo_legislatura' : legislatura [1],
            'titulo_legislatura' : legislatura[0],
            'presidente' : legislatura[2],
            'numero_leyes' : legislatura[3]
        }
        legislatura_array.append(ley)
    if len(legislatura_array) == 0:
        raise Http404

    return HttpResponse(json.dumps(legislatura_array), content_type="application/json")

def leyes_legislatura(request):
    cursor = connection.cursor()
    cursor.execute('SELECT legislatura, cod_legislatura, sum(n_leyes), presidente from materias_legislaturas '
                      'group by legislatura, cod_legislatura, presidente '
                      'order by  cod_legislatura')
    legislatura_array = []
    for legislatura in cursor.fetchall():

        ley = {

            'codigo_legislatura' : legislatura [1],
            'titulo_legislatura' : legislatura[0],
            'presidente' : legislatura[3],
            'numero_leyes' : legislatura[2]
        }
        legislatura_array.append(ley)
    if len(legislatura_array) == 0:
        raise Http404
    return HttpResponse(json.dumps(legislatura_array), content_type="application/json")


def leyes_meses_legislatura(request):
    cursor = connection.cursor()
    cursor.execute('SELECT '
                   'nombre_legislatura, presidente,'
                   'legislatura_id, anyo, mes, num_leyes from leyes_mes '

                      'order by  legislatura_id')
    legislatura_array = []
    for legislatura in cursor.fetchall():
        ley = {

            'codigo_legislatura' : legislatura [2],
            'titulo_legislatura' : legislatura[0],
            'presidente' : legislatura[1],
            'anyo' : legislatura[3],
            'mes' : legislatura[4],
            'numero_leyes' : legislatura[5]
        }
        legislatura_array.append(ley)
    if len(legislatura_array) == 0:
        raise Http404
    return HttpResponse(json.dumps(legislatura_array), content_type="application/json")





def materias_legislatura(request, materias):

    cursor = connection.cursor()

    cursor.execute('SELECT * from materias_legislaturas where codigo_materia = %s;', [materias])

    legislatura_array = []

    for legislatura in cursor.fetchall():
        ley = {
            'titulo_materia' : legislatura[0],
            'codigo_materia' : legislatura[1],
            'codigo_legislatura' : legislatura[2],
            'titulo_legislatura' : legislatura[3],
            'presidente' : legislatura[4],
            'numero_leyes' : legislatura[5]
        }
        legislatura_array.append(ley)
    if len(legislatura_array) == 0:
        raise Http404
    return HttpResponse(json.dumps(legislatura_array), content_type="application/json")


def top_materias(request):

    cursor = connection.cursor()
    cursor.execute('SELECT codigo_materia, titulo_materia, sum(n_leyes) as total from materias_legislaturas group by codigo_materia, titulo_materia order by total desc limit 50;')
    materias = []
    for entrada in cursor.fetchall():
        materia = {
            'codigo_materia': entrada[0],
            'titulo_materia': entrada[1],
            'total': entrada[2]
        }
        materias.append(materia)
    if len(materias) == 0:
        raise Http404
    return HttpResponse(json.dumps(materias), content_type="application/json")


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




