from django.conf.urls import patterns, include, url
from django.contrib import admin


# admin.site.register(boe_analisis)


urlpatterns = patterns('',
    url(r'^listado/$', 'boe_analisis.views.home'),
    url(r'^(?P<identificador>[\w|\-]+)$', 'boe_analisis.views.individual'),
                       )