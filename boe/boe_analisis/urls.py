from django.conf.urls import patterns, include, url
from django.contrib import admin


# admin.site.register(boe_analisis)


urlpatterns = patterns('',
    url(r'^listado/$', 'boe_analisis.views.home'),
    url(r'^(?P<identificador>[\w|\-]+)$', 'boe_analisis.views.individual'),
    url(r'^materias/(?P<materia>[\w|\-]+)/$', 'boe_analisis.views.materias'),
    url(r'^materias/$', 'boe_analisis.views.listado_materias'),
    url(r'^graficos/$', 'boe_analisis.views.graficos'),
                       )