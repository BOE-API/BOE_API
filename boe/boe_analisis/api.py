__author__ = 'Carlos'
from boe_analisis.models import Materia, Documento, Diario, Origen_legislativo
from boe_analisis.models import Departamento, Rango, Legislatura, Estado_consolidacion
from tastypie.resources import ModelResource, Bundle
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from django.conf.urls import url
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from tastypie.utils import trailing_slash
from django.core.cache import cache
class DepartamentoResource(ModelResource):
    class Meta:
        queryset = Departamento.objects.all()
        resource_name = 'departamento'
        list_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()

class RangoResource(ModelResource):
    class Meta:
        queryset = Rango.objects.all()
        resource_name = 'rango'
        list_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
    def determine_format(self, request):
        return 'application/json'


class LegislaturaResource(ModelResource):
    class Meta:
        queryset = Legislatura.objects.all()
        resource_name = 'legislatura'
        list_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
    def determine_format(self, request):
        return 'application/json'

#
class Estado_consolidacionResource(ModelResource):
    class Meta:
        queryset = Estado_consolidacion.objects.all()
        resource_name = 'estado_consolidacion'
        list_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
    def determine_format(self, request):
        return 'application/json'


class Origen_legislativoResource(ModelResource):
    class Meta:
        queryset = Origen_legislativo.objects.all()
        resource_name = 'origen_legislativo'
        list_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
    def determine_format(self, request):
        return 'application/json'




class MateriaResource(ModelResource):
    class Meta:
        queryset = Materia.objects.all()
        resource_name = 'materia'
        list_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        filtering = {
            'titulo': ALL,
        }
    def determine_format(self, request):
        return 'application/json'


class DiarioResource(ModelResource):
    class Meta:
        queryset = Diario.objects.all()
        resource_name = 'diario'
        list_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
    def determine_format(self, request):
        return 'application/json'


class DocumentoResource(ModelResource):
    diario_numero = fields.ForeignKey(DiarioResource, 'diario', full=True)
    materias = fields.ToManyField(MateriaResource, 'materias', full=True)
    departamento = fields.ForeignKey(DepartamentoResource, 'departamento', full=True, null=True,blank=True)
    origen_legislativo = fields.ForeignKey(Origen_legislativoResource, 'origen_legislativo', full=True, null=True,blank=True)
    estado_consolidacion = fields.ForeignKey(Estado_consolidacionResource, 'estado_consolidacion', full=True, null=True,blank=True)
    rango = fields.ForeignKey(RangoResource, 'rango', full=True, null=True,blank=True)
    legislatura = fields.ForeignKey(LegislaturaResource, 'legislatura', full=True, null=True,blank=True)
    search = None
    last_query = ''


    class Meta:
        queryset = Documento.objects.all()
        resource_name = 'documento'
        api_name = 'v1',
        detail_uri_name = 'identificador'
        list_allowed_methods = ['get', 'post']
        filtering = {
            'titulo': ALL,
            'identificador': ALL,
            'fecha_publicacion': ALL,
            'materias': ALL_WITH_RELATIONS,
        }
        authorization = DjangoAuthorization()
    def determine_format(self, request):
        return 'application/json'
    def prepend_urls(self):
        return [url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),]
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        actualQuery = request.GET.get('q', '')
        # Do the query.
        print self.last_query
        print actualQuery
        if self.last_query != actualQuery:
            sqs = SearchQuerySet().models(Documento).load_all().auto_query(request.GET.get('q', ''))
            print len(sqs)
            paginator = Paginator(sqs, 20)
            self.last_query = actualQuery
            self.search = paginator
        else:
            print 'guardado'
            paginator = self.search


        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)