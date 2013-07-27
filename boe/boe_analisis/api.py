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
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from tastypie.utils import trailing_slash
from tastypie import resources
from django.http import HttpResponse
from django.core.cache import cache
from tastypie.paginator import Paginator



def build_content_type(format, encoding='utf-8'):
    """
    Appends character encoding to the provided format if not already present.
    """
    print format
    if 'charset' in format:
        return format

    return "%s; charset=%s" % (format, encoding)

class MyModelResource(resources.ModelResource):
    def create_response(self, request, data, response_class=HttpResponse, **response_kwargs):
        """
        Extracts the common "which-format/serialize/return-response" cycle.

        Mostly a useful shortcut/hook.
        """
        desired_format = self.determine_format(request)
        serialized = self.serialize(request, data, desired_format)
        return response_class(content=serialized, content_type=build_content_type(desired_format), **response_kwargs)


class PageNumberPaginator(Paginator):
    def page(self):
        output = super(PageNumberPaginator, self).page()
        output['page'] = int(self.offset / self.limit) + 1
        return output

class DepartamentoResource(MyModelResource):
    class Meta:
        queryset = Departamento.objects.all()
        resource_name = 'departamento'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()

class RangoResource(MyModelResource):
    class Meta:
        queryset = Rango.objects.all()
        resource_name = 'rango'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
    def determine_format(self, request):
        return 'application/json'


class PartidoResource(MyModelResource):
    class Meta:
        queryset = Partido.objects.all()
        resource_name = 'partido'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
    def determine_format(self, request):
        return 'application/json'


class LegislaturaResource(MyModelResource):
    class Meta:
        queryset = Legislatura.objects.all()
        resource_name = 'legislatura'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
    def determine_format(self, request):
        return 'application/json'


class Estado_consolidacionResource(MyModelResource):
    class Meta:
        queryset = Estado_consolidacion.objects.all()
        resource_name = 'estado_consolidacion'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
    def determine_format(self, request):
        return 'application/json'


class Origen_legislativoResource(MyModelResource):
    class Meta:
        queryset = Origen_legislativo.objects.all()
        resource_name = 'origen_legislativo'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
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
    def determine_format(self, request):
        return 'application/json'


class DiarioResource(MyModelResource):
    class Meta:
        queryset = Diario.objects.all()
        resource_name = 'diario'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()


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
    def determine_format(self, request):
        return 'application/json'

class PalabraResource(MyModelResource):
    class Meta:
        queryset = Palabra.objects.all()
        resource_name = 'palabra'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
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
        queryset = Documento.objects.exclude(url_xml=None).select_related()
        resource_name = 'documento'
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
        paginator_class = Paginator
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
        paginator_class = Paginator

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
        paginator_class = Paginator
