from django.db import models

# Create your models here.


class Diario(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    titulo = models.CharField(max_length=200, null=True)

class Departamento(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    titulo = models.CharField(max_length=200, null=True)

class Rango(models.Model):
    codigo = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=200, null=True )

class Origen_legislativo(models.Model):
    codigo = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=200, null=True)

class Estado_consolidacion(models.Model):
    codigo = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=200, null=True)

class Nota(models.Model):
    codigo = models.IntegerField()
    titulo = models.CharField(max_length=200, null=True)

    class Meta:
        unique_together = (('codigo', 'titulo'),)

class Materia(models.Model):
    codigo = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=200, null=True)


class Alerta(models.Model):
    codigo = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=200, null=True)

class Palabra(models.Model):
    codigo = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=200, null=True)

class Referencia(models.Model):
    referencia = models.ForeignKey('Documento')
    palabra = models.ForeignKey(Palabra)
    texto = models.TextField(max_length=4000)

    class Meta:
        unique_together = (('referencia','palabra'),)

    # def __unicode__(self):
    #     return self.palabra.codigo

class Documento(models.Model):

    identificador = models.CharField(max_length=25, primary_key=True)
    titulo = models.CharField(null=True, max_length=1500)
    diario = models.ForeignKey(Diario, null=True)
    diario_numero = models.IntegerField(null=True)
    seccion = models.CharField(max_length=50, null=True)
    subseccion = models.CharField(max_length=50, null=True)
    rango = models.ForeignKey(Rango, null=True)
    departamento = models.ForeignKey(Departamento, null=True)
    numero_oficial = models.CharField(max_length=50, null=True)
    fecha_disposicion = models.DateField(null=True)
    fecha_publicacion = models.DateField(null=True)
    fecha_vigencia = models.DateField(null=True)
    fecha_derogacion = models.DateField(null=True)
    letra_imagen = models.CharField(max_length=10, null=True)
    pagina_inicial = models.IntegerField(null=True)
    pagina_final = models.IntegerField(null=True)
    suplemento_letra_imagen = models.CharField(max_length=10, null=True)
    suplemento_pagina_inicial = models.CharField(max_length=10, null=True)
    suplemento_pagina_final = models.CharField(max_length=10, null=True)
    estatus_legislativo = models.CharField(max_length=10, null=True)
    origen_legislativo = models.ForeignKey(Origen_legislativo, null=True)
    estado_consolidacion = models.ForeignKey(Estado_consolidacion, null=True)
    judicialmente_anulada = models.NullBooleanField(null=True)
    vigencia_agotada = models.NullBooleanField(null=True)

    url_epub = models.URLField(null=True)
    url_xml = models.URLField(null=True)
    url_htm = models.URLField(null=True)
    url_pdf = models.URLField(null=True)
    url_pdf_catalan = models.URLField(null=True)
    url_pdf_euskera = models.URLField(null=True)
    url_pdf_gallego = models.URLField(null=True)
    url_pdf_valenciano = models.URLField(null=True)
    notas = models.ManyToManyField(Nota)
    materias = models.ManyToManyField(Materia)
    alertas = models.ManyToManyField(Alerta)
    referencias_anteriores = models.ManyToManyField(Referencia, related_name='ref_anteriores')
    referencias_posteriores = models.ManyToManyField(Referencia, related_name='ref_posteriores')
    texto = models.TextField(null=True)

    def __unicode__(self):
        return self.identificador