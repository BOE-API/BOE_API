__author__ = 'Carlos'
from boe_analisis.models import Materia, Documento, Diario, Origen_legislativo
from boe_analisis.models import Nota, Palabra, Referencia, Alerta
from boe_analisis.models import Departamento, Partido, Rango, Legislatura, Estado_consolidacion
from tastypie.resources import ModelResource, Bundle
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authorization import DjangoAuthorization, ReadOnlyAuthorization
from tastypie.authentication import ApiKeyAuthentication, BasicAuthentication
from django.conf.urls import url
from haystack.query import SearchQuerySet
# from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from tastypie.utils import trailing_slash
from tastypie import resources, Resource
from tastypie.exceptions import  import ImmediateHttpResponse
from django.http import HttpResponse
from django.core.cache import cache
from tastypie.paginator import Paginator
from tastypie import http
from boe_analisis.paginator import ModelPagination
from tastypie.cache import SimpleCache
import json

from django.db import connection

from tastypie.paginator import Paginator

class BaseCorsResource(Resource):
    """
    Class implementing CORS
    """
    def create_response(self, *args, **kwargs):
        response = super(BaseCorsResource, self).create_response(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    def method_check(self, request, allowed=None):
        if allowed is None:
            allowed = []

        request_method = request.method.lower()
        allows = ','.join(map(str.upper, allowed))

        if request_method == 'options':
            response = HttpResponse(allows)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        if not request_method in allowed:
            response = http.HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        return request_method


def build_content_type(format, encoding='utf-8'):
    """
    Appends character encoding to the provided format if not already present.
    """
    print format
    if 'charset' in format:
        return format

    return "%s; charset=%s" % (format, encoding)

class MyModelResource(BaseCorsResource, resources.ModelResource):

    def create_response(self, request, data, response_class=HttpResponse, **response_kwargs):
        """
        Extracts the common "which-format/serialize/return-response" cycle.

        Mostly a useful shortcut/hook.
        """
        desired_format = self.determine_format(request)
        serialized = self.serialize(request, data, desired_format)
        return response_class(content=serialized, content_type=build_content_type(desired_format), **response_kwargs)

class EstimatedCountPaginator(Paginator):
    def __init__(self, request_data, objects, resource_uri=None, limit=None, offset=0, max_limit=1000, collection_name='objects'):

        super(EstimatedCountPaginator, self).__init__(request_data, objects, resource_uri, limit, offset, max_limit, collection_name)
        self.count = self.get_estimated_count()
    def get_next(self, limit, offset, count):
        # The parent method needs an int which is higher than "limit + offset"
        # to return a url. Setting it to an unreasonably large value, so that
        # the parent method will always return the url.
        count = 2 ** 64
        return super(EstimatedCountPaginator, self).get_next(limit, offset, count)

    def get_count(self):
        return None
    def get_next(self, limit, offset, count):
        print "COUNT"
        print self.count
        if limit + offset > self.count:
            if limit + offset >= self.get_max_id():

                return None
        offset = self.cached[limit-1:limit][0].id + 1
        print offset
        return self._generate_uri(limit, offset)
    def get_previous(self, limit, offset):
        print offset
        if offset > limit:
            offset = self.objects.filter(id__lt = offset).order_by('-id')[limit -1 :limit][0].id
        return self._generate_uri(limit, offset)
    # def _generate_uri(self, limit, offset):
    #     pass
    def get_slice(self, limit, offset):
        self.cached = self.objects.filter(id__gte = offset).order_by('id')[:limit]
        return self.cached


    def get_estimated_count(self):
        """Get the estimated count by using the database query planner."""
        # If you do not have PostgreSQL as your DB backend, alter this method
        # accordingly.
        return self._get_postgres_estimated_count()

    def get_max_id(self):
        cursor = connection.cursor()
        query = 'SELECT id FROM "boe_analisis_documento"  where url_xml is not null ORDER BY "boe_analisis_documento"."id" desc limit 1;'
        cursor.execute(query)

        self.max_id = cursor.fetchone()[0]
        print self.max_id
        return self.max_id
    def _get_postgres_estimated_count(self):

        # This method only works with postgres >= 9.0.
        # If you need postgres vesrions less than 9.0, remove "(format json)"
        # below and parse the text explain output.

        def _get_postgres_version():
            # Due to django connections being lazy, we need a cursor to make
            # sure the connection.connection attribute is not None.
            connection.cursor()
            return connection.connection.server_version

        try:
            if _get_postgres_version() < 90000:
                return
        except AttributeError:
            return

        cursor = connection.cursor()
        query = "select reltuples from pg_class where relname='boe_analisis_documento';"

        # # Remove limit and offset from the query, and extract sql and params.
        # query.low_mark = None
        # query.high_mark = None
        # query, params = self.objects.query.sql_with_params()
        #
        # # Fetch the estimated rowcount from EXPLAIN json output.
        # query = 'explain (format json) %s' % query
        cursor.execute(query)
        # print query
        rows = cursor.fetchone()[0]
        # # Older psycopg2 versions do not convert json automatically.
        # if isinstance(explain, basestring):
        #     explain = json.loads(explain)
        #     print explain
        # rows = explain[0]['Plan']['Plan Rows']
        return rows

    def page(self):
        self.max_id = None
        data = super(EstimatedCountPaginator, self).page()
        data['meta']['estimated_count'] = self.get_estimated_count()
        return data



class DepartamentoResource(MyModelResource):
    class Meta:
        queryset = Departamento.objects.all()
        resource_name = 'departamento'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        cache = SimpleCache(timeout=60*60*24)

class RangoResource(MyModelResource):
    class Meta:
        queryset = Rango.objects.all()
        resource_name = 'rango'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        cache = SimpleCache(timeout=60*60*24)
    def determine_format(self, request):
        return 'application/json'


class PartidoResource(MyModelResource):
    class Meta:
        queryset = Partido.objects.all()
        resource_name = 'partido'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        cache = SimpleCache(timeout=60*60*24)
    def determine_format(self, request):
        return 'application/json'


class LegislaturaResource(MyModelResource):
    class Meta:
        queryset = Legislatura.objects.all()
        resource_name = 'legislatura'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        cache = SimpleCache(timeout=60*60*24)
    def determine_format(self, request):
        return 'application/json'


class Estado_consolidacionResource(MyModelResource):
    class Meta:
        queryset = Estado_consolidacion.objects.all()
        resource_name = 'estado_consolidacion'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        cache = SimpleCache(timeout=60*60*24)
    def determine_format(self, request):
        return 'application/json'


class Origen_legislativoResource(MyModelResource):
    class Meta:
        queryset = Origen_legislativo.objects.all()
        resource_name = 'origen_legislativo'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        cache = SimpleCache(timeout=60*60*24)
    def determine_format(self, request):
        return 'application/json'




class MateriaResource(MyModelResource):
    class Meta:
        queryset = Materia.objects.all()
        resource_name = 'materia'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        filtering = {
            'titulo': ALL,
        }
        cache = SimpleCache(timeout=60*60*24)
    def determine_format(self, request):
        return 'application/json'


class DiarioResource(MyModelResource):
    class Meta:
        queryset = Diario.objects.all()
        resource_name = 'diario'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        cache = SimpleCache(timeout=60*60*24)

    def determine_format(self, request):
        return 'application/json'


class NotaResource(MyModelResource):
    class Meta:
        queryset = Nota.objects.all()
        resource_name = 'nota'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
    def determine_format(self, request):
        return 'application/json'

class AlertaResource(MyModelResource):
    class Meta:
        queryset = Alerta.objects.all()
        resource_name = 'alerta'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        cache = SimpleCache(timeout=60*60*24)
    def determine_format(self, request):
        return 'application/json'

class PalabraResource(MyModelResource):
    class Meta:
        queryset = Palabra.objects.all()
        resource_name = 'palabra'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        cache = SimpleCache(timeout=60*60*24)
    def determine_format(self, request):
        return 'application/json'

class ReferenciaResource(MyModelResource):

    # referencia = fields.ForeignKey('DocumentoResource', null=True, blank=True)
    # palabra = fields.ForeignKey(PalabraResource, null=True, blank=True)
    class Meta:
        queryset = Referencia.objects.all()
        resource_name = 'referencia'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        cache = SimpleCache(timeout=60*60*24)
    def determine_format(self, request):
        return 'application/json'

class DocumentoResource(MyModelResource):
    diario = fields.ForeignKey(DiarioResource,
                                      'diario',
                                      full=True,
                                      null=True,
                                      blank=True,

                                      help_text="Codigo del Diario")
    materias = fields.ToManyField(MateriaResource,
                                  'materias',
                                  full=True,
                                  null=True,
                                  blank=True,
                                  help_text="Materias del documento")
    departamento = fields.ForeignKey(DepartamentoResource,
                                     'departamento',
                                     full=True,
                                     null=True,
                                     blank=True,
                                     help_text="Departamento del documento")
    origen_legislativo = fields.ForeignKey(Origen_legislativoResource,
                                           'origen_legislativo',
                                           full=True,
                                           null=True,
                                           blank=True,
                                           help_text="Origen Legislativo")
    estado_consolidacion = fields.ForeignKey(Estado_consolidacionResource,
                                             'estado_consolidacion',
                                             full=True,
                                             null=True,
                                             blank=True,
                                             help_text="Estado de consolidacion")
    rango = fields.ForeignKey(RangoResource,
                            'rango',
                            full=True,
                            null=True,
                            blank=True,
                            help_text="Rango del Documento(Ley, Real Decreto...)")
    legislatura = fields.ForeignKey(LegislaturaResource,
                                    'legislatura',
                                    full=True,
                                    null=True,
                                    blank=True,
                                    help_text="Legislatura de disposicion de la ley")


    alertas = fields.ToManyField(AlertaResource, 'alertas', full=True,
                                    null=True, blank=True)
    notas = fields.ToManyField(NotaResource, 'notas', full=True,
                               null=True, blank=True)


    referencias_anteriores = fields.ToManyField('boe_analisis.api.ReferenciaResource', 'referencias_anteriores',full=True,
                                   null=True, blank=True,
                                   related_name='ref_anteriores')
    referencias_posteriores = fields.ToManyField('boe_analisis.api.ReferenciaResource', 'referencias_posteriores', full=True,
                                   null=True, blank=True,
                                   related_name='ref_posteriores')

    search = None
    last_query = ''


    class Meta:
        last_id = 0
        queryset = Documento.objects.exclude(url_xml=None)
        resource_name = 'documento'
        api_name = 'v1',
        detail_uri_name = 'identificador'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        ordering = ['id']
        filtering = {
            'titulo': ALL,
            'identificador': ALL,
            'fecha_publicacion': ALL,
            'diario': ALL_WITH_RELATIONS,
            'materias': ALL_WITH_RELATIONS,
            'legislatura': ALL_WITH_RELATIONS,
            'notas': ALL_WITH_RELATIONS,
            'referencias_anteriores': ALL_WITH_RELATIONS,
            'referencias_posteriores': ALL_WITH_RELATIONS,

        }
        # authentication = BasicAuthentication()
        authorization = ReadOnlyAuthorization()
        paginator_class = EstimatedCountPaginator
        cache = SimpleCache(timeout=60*60*24)
    def determine_format(self, request):
        return 'application/json'






class BOEResource(DocumentoResource):


    class Meta:
        queryset = Documento.objects.exclude(url_xml=None).filter(diario = 'BOE')
        resource_name = 'documentoboe'
        api_name = 'v1',
        detail_uri_name = 'identificador'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        filtering = {
            'titulo': ALL,
            'identificador': ALL,
            'fecha_publicacion': ALL,
            'diario': ALL_WITH_RELATIONS,
            'materias': ALL_WITH_RELATIONS,
            'legislatura': ALL_WITH_RELATIONS,
            'notas': ALL_WITH_RELATIONS,
            'referencias_anteriores': ALL_WITH_RELATIONS,
            'referencias_posteriores': ALL_WITH_RELATIONS,

        }
        # authentication = BasicAuthentication()
        authorization = ReadOnlyAuthorization()
        paginator_class = EstimatedCountPaginator
        cache = SimpleCache(timeout=60*60*24)

class BORMEResource(DocumentoResource):


    class Meta:
        queryset = Documento.objects.exclude(url_xml=None).filter(diario = 'BORME')
        resource_name = 'documentoborme'
        api_name = 'v1',
        detail_uri_name = 'identificador'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        filtering = {
            'titulo': ALL,
            'identificador': ALL,
            'fecha_publicacion': ALL,
            'diario': ALL_WITH_RELATIONS,

        }
        # authentication = BasicAuthentication()
        authorization = ReadOnlyAuthorization()
        paginator_class = EstimatedCountPaginator
        cache = SimpleCache(timeout=60*60*24)
