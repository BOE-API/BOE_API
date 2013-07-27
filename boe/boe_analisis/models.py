# -*- coding: utf-8 -*-
from django.db import models
import datetime

# Create your models here.


class Diario(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    titulo = models.CharField(max_length=400, null=True)

class Departamento(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    titulo = models.CharField(max_length=4000, null=True)

class Rango(models.Model):
    codigo = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=4000, null=True )

class Origen_legislativo(models.Model):
    codigo = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=4000, null=True)

class Estado_consolidacion(models.Model):
    codigo = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=4000, null=True)

class Nota(models.Model):
    codigo = models.IntegerField()
    titulo = models.CharField(max_length=4000, null=True)

    class Meta:
        unique_together = (('codigo', 'titulo'),)

class Materia(models.Model):
    codigo = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=4000, null=True)


class Alerta(models.Model):
    codigo = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=4000, null=True)

class Palabra(models.Model):
    codigo = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=4000, null=True)

class Referencia(models.Model):
    referencia = models.ForeignKey('Documento')
    palabra = models.ForeignKey(Palabra)
    texto = models.TextField(max_length=4000)

    class Meta:
        unique_together = (('referencia','palabra'),)

    # def __unicode__(self):
    #     return self.palabra.codigo

class Partido(models.Model):

    nombre = models.CharField(max_length=200)

    def __unicode__(self):
        return self.nombre

class Legislatura(models.Model):
    inicio = models.DateField()
    final = models.DateField(null=True, blank=True)
    partido = models.ForeignKey(Partido)
    presidente = models.CharField(max_length=300)
    nombre_legislatura = models.CharField(max_length=600)

    class Meta:
        ordering = ['inicio']

    def __unicode__(self):
        return self.nombre_legislatura




class Documento(models.Model):

    identificador = models.CharField(max_length=25,
                                     db_index=True,
                                     unique=True,
                                     help_text="Identificador oficial del documento")
    titulo = models.CharField(null=True,
                              max_length=5000,
                              default='',
                              db_index=True,
                              help_text="Titulo del documento")
    diario = models.ForeignKey(Diario, null=True)
    diario_numero = models.IntegerField(null=True,
                                        help_text="Corresponde al número del diario"
                                                  " en el que se publicó la norma. "
                                                  "Es un número correlativo que comienza cada año."
                                                  )
    seccion = models.CharField(max_length=50,
                               null=True,
                               default='',
                               help_text="Sección")
    subseccion = models.CharField(max_length=50,
                                  null=True,
                                  default='',
                                  help_text="Subsección")
    rango = models.ForeignKey(Rango,
                              null=True,
                              help_text="Categoría normativa de la disposición: "
                                        "Ley, Real Decreto, Orden, Directiva,"
                                        " etcétera.")
    departamento = models.ForeignKey(Departamento, null=True,
                                     help_text="Organismo que emite la resolución.")
    numero_oficial = models.CharField(max_length=50,
                                      null=True,
                                      default='',
                                      help_text="Es el número de la norma, "
                                                "tiene estructura de número/año."
                                                " Ejemplo: 169/2008")
    fecha_disposicion = models.DateField(null=True,
                                         help_text="Es la fecha en la que se aprueba la norma.")
    fecha_publicacion = models.DateField(null=True, db_index=True,
                                         help_text="Es la fecha del BOE o DOUE"
                                                   " en la que se publicó la norma.")
    fecha_vigencia = models.DateField(null=True,
                                      help_text="Fecha en la que entra en vigor la norma")
    fecha_derogacion = models.DateField(null=True,
                                        help_text="Fecha en la que la norma de deroga")
    letra_imagen = models.CharField(max_length=10, null=True, default='',
                                    help_text="-")
    pagina_inicial = models.IntegerField(null=True,
                                         help_text="Pagina inicial")
    pagina_final = models.IntegerField(null=True,
                                       help_text="Pagina final")
    suplemento_letra_imagen = models.CharField(max_length=10,
                                               null=True,
                                               default='',
                                               help_text="-")
    suplemento_pagina_inicial = models.CharField(max_length=10,
                                                 null=True,
                                                 default='',
                                                 help_text="-")
    suplemento_pagina_final = models.CharField(max_length=10,
                                               null=True,
                                               default='',
                                               help_text="-")
    estatus_legislativo = models.CharField(max_length=10,
                                           null=True,
                                           default='',
                                           help_text="-")
    origen_legislativo = models.ForeignKey(Origen_legislativo,
                                           null=True,
                                           help_text="Autonomico, Estatal o Europeo")
    estado_consolidacion = models.ForeignKey(Estado_consolidacion,
                                             null=True,
                                             help_text="Desactualizado, Finalizado o En proceso")
    judicialmente_anulada = models.NullBooleanField(null=True,
                                                    help_text="Anulada judicialmente")
    vigencia_agotada = models.NullBooleanField(null=True,
                                               help_text="Con vigencia agotada")
    legislatura = models.ForeignKey(Legislatura,null=True,
                                    help_text="Legislatura en la que se aprobó la norma")
    url_epub = models.URLField(null=True,
                               help_text="URL EPUB")
    url_xml = models.URLField(null=True, db_index=True,
                              help_text="URL XML")
    url_htm = models.URLField(null=True,
                              help_text="URL HTML")
    url_pdf = models.URLField(null=True,
                              help_text="URL PDF")
    url_pdf_catalan = models.URLField(null=True,
                                      help_text="URL PDF Catalan (No todos los documentos los tienen)")
    url_pdf_euskera = models.URLField(null=True,
                                       help_text="URL PDF Euskera (No todos los documentos los tienen)")
    url_pdf_gallego = models.URLField(null=True,
                                       help_text="URL PDF Gallego (No todos los documentos los tienen)")
    url_pdf_valenciano = models.URLField(null=True,
                                          help_text="URL PDF Valenciano (No todos los documentos los tienen)")
    notas = models.ManyToManyField(Nota,
                                   help_text="Notas del documento")
    materias = models.ManyToManyField(Materia,
                                      help_text="Materias del documento")
    alertas = models.ManyToManyField(Alerta,
                                     help_text="Alertas disponibles para el documento")
    referencias_anteriores = models.ManyToManyField(Referencia,
                                                    related_name='ref_anteriores',
                                                    help_text="Referencias anteriores")
    referencias_posteriores = models.ManyToManyField(Referencia,
                                                     related_name='ref_posteriores',
                                                     help_text="Referencias posteriores")
    texto = models.TextField(null=True, default='',
                             help_text="Texto del documento en HTML")

    def __unicode__(self):
        return self.identificador
    class Meta:
        ordering = ['-fecha_publicacion']
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('individual_doc', args=[str(self.identificador)])