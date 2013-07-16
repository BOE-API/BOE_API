# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Estado_consolidacion.titulo'
        db.alter_column(u'boe_analisis_estado_consolidacion', 'titulo', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Nota.titulo'
        db.alter_column(u'boe_analisis_nota', 'titulo', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Alerta.titulo'
        db.alter_column(u'boe_analisis_alerta', 'titulo', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Palabra.titulo'
        db.alter_column(u'boe_analisis_palabra', 'titulo', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Rango.titulo'
        db.alter_column(u'boe_analisis_rango', 'titulo', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Materia.titulo'
        db.alter_column(u'boe_analisis_materia', 'titulo', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Origen_legislativo.titulo'
        db.alter_column(u'boe_analisis_origen_legislativo', 'titulo', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Diario.titulo'
        db.alter_column(u'boe_analisis_diario', 'titulo', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Departamento.titulo'
        db.alter_column(u'boe_analisis_departamento', 'titulo', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    def backwards(self, orm):

        # Changing field 'Estado_consolidacion.titulo'
        db.alter_column(u'boe_analisis_estado_consolidacion', 'titulo', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Nota.titulo'
        db.alter_column(u'boe_analisis_nota', 'titulo', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Alerta.titulo'
        db.alter_column(u'boe_analisis_alerta', 'titulo', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Palabra.titulo'
        db.alter_column(u'boe_analisis_palabra', 'titulo', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Rango.titulo'
        db.alter_column(u'boe_analisis_rango', 'titulo', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Materia.titulo'
        db.alter_column(u'boe_analisis_materia', 'titulo', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Origen_legislativo.titulo'
        db.alter_column(u'boe_analisis_origen_legislativo', 'titulo', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Diario.titulo'
        db.alter_column(u'boe_analisis_diario', 'titulo', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Departamento.titulo'
        db.alter_column(u'boe_analisis_departamento', 'titulo', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

    models = {
        u'boe_analisis.alerta': {
            'Meta': {'object_name': 'Alerta'},
            'codigo': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        u'boe_analisis.departamento': {
            'Meta': {'object_name': 'Departamento'},
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        u'boe_analisis.diario': {
            'Meta': {'object_name': 'Diario'},
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        u'boe_analisis.documento': {
            'Meta': {'object_name': 'Documento'},
            'alertas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['boe_analisis.Alerta']", 'symmetrical': 'False'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boe_analisis.Departamento']", 'null': 'True'}),
            'diario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boe_analisis.Diario']", 'null': 'True'}),
            'diario_numero': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'estado_consolidacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boe_analisis.Estado_consolidacion']", 'null': 'True'}),
            'estatus_legislativo': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'fecha_derogacion': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'fecha_disposicion': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'fecha_publicacion': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'fecha_vigencia': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'identificador': ('django.db.models.fields.CharField', [], {'max_length': '25', 'primary_key': 'True'}),
            'judicialmente_anulada': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'letra_imagen': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'materias': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['boe_analisis.Materia']", 'symmetrical': 'False'}),
            'notas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['boe_analisis.Nota']", 'symmetrical': 'False'}),
            'numero_oficial': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'origen_legislativo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boe_analisis.Origen_legislativo']", 'null': 'True'}),
            'pagina_final': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pagina_inicial': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'rango': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boe_analisis.Rango']", 'null': 'True'}),
            'referencias_anteriores': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ref_anteriores'", 'symmetrical': 'False', 'to': u"orm['boe_analisis.Referencia']"}),
            'referencias_posteriores': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ref_posteriores'", 'symmetrical': 'False', 'to': u"orm['boe_analisis.Referencia']"}),
            'seccion': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'subseccion': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'suplemento_letra_imagen': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'suplemento_pagina_final': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'suplemento_pagina_inicial': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'texto': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'url_epub': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'url_htm': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'url_pdf': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'url_pdf_catalan': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'url_pdf_euskera': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'url_pdf_gallego': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'url_pdf_valenciano': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'url_xml': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'vigencia_agotada': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        u'boe_analisis.estado_consolidacion': {
            'Meta': {'object_name': 'Estado_consolidacion'},
            'codigo': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        u'boe_analisis.materia': {
            'Meta': {'object_name': 'Materia'},
            'codigo': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        u'boe_analisis.nota': {
            'Meta': {'unique_together': "(('codigo', 'titulo'),)", 'object_name': 'Nota'},
            'codigo': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        u'boe_analisis.origen_legislativo': {
            'Meta': {'object_name': 'Origen_legislativo'},
            'codigo': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        u'boe_analisis.palabra': {
            'Meta': {'object_name': 'Palabra'},
            'codigo': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        u'boe_analisis.rango': {
            'Meta': {'object_name': 'Rango'},
            'codigo': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        u'boe_analisis.referencia': {
            'Meta': {'unique_together': "(('referencia', 'palabra'),)", 'object_name': 'Referencia'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'palabra': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boe_analisis.Palabra']"}),
            'referencia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boe_analisis.Documento']"}),
            'texto': ('django.db.models.fields.TextField', [], {'max_length': '4000'})
        }
    }

    complete_apps = ['boe_analisis']