# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Documento', fields ['identificador']
        db.create_unique(u'boe_analisis_documento', ['identificador'])


    def backwards(self, orm):
        # Removing unique constraint on 'Documento', fields ['identificador']
        db.delete_unique(u'boe_analisis_documento', ['identificador'])


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
            'estatus_legislativo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'null': 'True'}),
            'fecha_derogacion': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'fecha_disposicion': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'fecha_publicacion': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_index': 'True'}),
            'fecha_vigencia': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificador': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25', 'db_index': 'True'}),
            'judicialmente_anulada': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'legislatura': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boe_analisis.Legislatura']", 'null': 'True'}),
            'letra_imagen': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'null': 'True'}),
            'materias': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['boe_analisis.Materia']", 'symmetrical': 'False'}),
            'notas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['boe_analisis.Nota']", 'symmetrical': 'False'}),
            'numero_oficial': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True'}),
            'origen_legislativo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boe_analisis.Origen_legislativo']", 'null': 'True'}),
            'pagina_final': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pagina_inicial': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'rango': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boe_analisis.Rango']", 'null': 'True'}),
            'referencias_anteriores': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ref_anteriores'", 'symmetrical': 'False', 'to': u"orm['boe_analisis.Referencia']"}),
            'referencias_posteriores': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ref_posteriores'", 'symmetrical': 'False', 'to': u"orm['boe_analisis.Referencia']"}),
            'seccion': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True'}),
            'subseccion': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True'}),
            'suplemento_letra_imagen': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'null': 'True'}),
            'suplemento_pagina_final': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'null': 'True'}),
            'suplemento_pagina_inicial': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'null': 'True'}),
            'texto': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1500', 'null': 'True', 'db_index': 'True'}),
            'url_epub': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'url_htm': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'url_pdf': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'url_pdf_catalan': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'url_pdf_euskera': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'url_pdf_gallego': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'url_pdf_valenciano': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'url_xml': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'db_index': 'True'}),
            'vigencia_agotada': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        u'boe_analisis.estado_consolidacion': {
            'Meta': {'object_name': 'Estado_consolidacion'},
            'codigo': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        u'boe_analisis.legislatura': {
            'Meta': {'object_name': 'Legislatura'},
            'final': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateField', [], {}),
            'partido': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boe_analisis.Partido']"})
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
        u'boe_analisis.partido': {
            'Meta': {'object_name': 'Partido'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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