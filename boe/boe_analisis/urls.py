from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from boe_analisis import views
# admin.site.register(boe_analisis)





urlpatterns = patterns('',
    url(r'^$', 'boe_analisis.views.home', name='home_docs'),
    # url(r'^api/$', include(router.urls)),
    url(r'^documento/(?P<identificador>[\w|\-]+)$', 'boe_analisis.views.individual', name="individual_doc"),
    url(r'^materias/(?P<materia>[\w|\-]+)/$', 'boe_analisis.views.materias' , name="individual_materia"),
    url(r'^materias/$', 'boe_analisis.views.listado_materias', name='listado_materias'),
    url(r'^graficos/$', 'boe_analisis.views.graficos', name='graficos'),
                       )