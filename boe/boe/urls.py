from boe_analisis.models import Documento, Diario
from boe_analisis.urls import *
from django.conf.urls import patterns, include, url
from rest_framework import viewsets, routers
from boe_analisis import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()
admin.site.register(Documento)


router = routers.DefaultRouter()
router.register(r'documentos', views.DocumentoViewSet)
router.register(r'diarios', views.DiarioViewSet)
router.register(r'materias', views.MateriaViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'boe.views.home', name='home'),
    url(r'^', include('boe_analisis.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),



    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', include('haystack.urls')),
)
