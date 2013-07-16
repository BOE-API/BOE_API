# Create your views here.
from django.template import RequestContext
from django.shortcuts import render,render_to_response, redirect
from django.shortcuts import get_object_or_404
from boe_analisis.models import Documento
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import *
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    documents = Documento.objects.exclude(titulo = None)
    paginator = Paginator(documents, 25)
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
