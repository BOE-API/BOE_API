from django.conf.urls import patterns, include, url
from django.contrib import admin
from boe_analisis.api import *
from django.contrib.auth.models import User
from boe_analisis import views
from tastypie.api import Api
from django.db import models
from tastypie.models import create_api_key
from django.views.decorators.cache import cache_page
# admin.site.register(boe_analisis)

v1_api = Api(api_name='v1')
v1_api.register(MateriaResource())
v1_api.register(DiarioResource())
v1_api.register(DocumentoResource())
v1_api.register(BOEResource())
v1_api.register(BORMEResource())
v1_api.register(NotaResource())
v1_api.register(AlertaResource())
v1_api.register(PalabraResource())
v1_api.register(ReferenciaResource())



v1_api.register(DepartamentoResource())
v1_api.register(RangoResource())
v1_api.register(LegislaturaResource())
v1_api.register(Estado_consolidacionResource())
v1_api.register(Origen_legislativoResource())
v1_api.register(PartidoResource())



urlpatterns = patterns('',
    url(r'^$', 'boe_analisis.views.home', name='home_docs'),
    url(r'^api/', (include(v1_api.urls))),
    url(r'^documento/(?P<identificador>[\w|\-]+)$', 'boe_analisis.views.individual', name="individual_doc"),
    url(r'^materias/(?P<materia>[\w|\-]+)/$', 'boe_analisis.views.materias' , name="individual_materia"),
    url(r'^materias/$', 'boe_analisis.views.listado_materias', name='listado_materias'),
    url(r'^graficos/$', 'boe_analisis.views.graficos', name='graficos'),
    url(r'^api/v1/years/$', ('boe_analisis.views.years')),
    url(r'^api/v1/years/materia/(?P<materia>\d+)$', 'boe_analisis.views.years'),
    url(r'^docs/', include("tastydocs.urls"), {"api": v1_api}) # api must be a reference to the TastyPie API object.

                       )

models.signals.post_save.connect(create_api_key, sender=User)