from boe_analisis.models import Documento, Diario, Partido, Legislatura
from boe_analisis.urls import *
from django.conf.urls import patterns, include, url
from boe_analisis import views
from social_networks.models import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
#
admin.autodiscover()
#admin.site.register(Documento)
#admin.site.register(Partido)
#admin.site.register(Legislatura)
admin.site.register(TwitterAccount)
admin.site.register(Word)
admin.site.register(FacebookAccount)
admin.site.register(Subject)



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'boe.views.home', name='home'),
    url(r'', include('boe_analisis.urls')),



    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^search/', include('haystack.urls')),
)
