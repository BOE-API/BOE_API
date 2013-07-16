# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Diario'
        db.create_table(u'boe_analisis_diario', (
            ('codigo', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'boe_analisis', ['Diario'])

        # Adding model 'Departamento'
        db.create_table(u'boe_analisis_departamento', (
            ('codigo', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'boe_analisis', ['Departamento'])

        # Adding model 'Rango'
        db.create_table(u'boe_analisis_rango', (
            ('codigo', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'boe_analisis', ['Rango'])

        # Adding model 'Origen_legislativo'
        db.create_table(u'boe_analisis_origen_legislativo', (
            ('codigo', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'boe_analisis', ['Origen_legislativo'])

        # Adding model 'Estado_consolidacion'
        db.create_table(u'boe_analisis_estado_consolidacion', (
            ('codigo', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'boe_analisis', ['Estado_consolidacion'])

        # Adding model 'Nota'
        db.create_table(u'boe_analisis_nota', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codigo', self.gf('django.db.models.fields.IntegerField')()),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'boe_analisis', ['Nota'])

        # Adding unique constraint on 'Nota', fields ['codigo', 'titulo']
        db.create_unique(u'boe_analisis_nota', ['codigo', 'titulo'])

        # Adding model 'Materia'
        db.create_table(u'boe_analisis_materia', (
            ('codigo', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'boe_analisis', ['Materia'])

        # Adding model 'Alerta'
        db.create_table(u'boe_analisis_alerta', (
            ('codigo', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'boe_analisis', ['Alerta'])

        # Adding model 'Palabra'
        db.create_table(u'boe_analisis_palabra', (
            ('codigo', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'boe_analisis', ['Palabra'])

        # Adding model 'Referencia'
        db.create_table(u'boe_analisis_referencia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('referencia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['boe_analisis.Documento'])),
            ('palabra', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['boe_analisis.Palabra'])),
            ('texto', self.gf('django.db.models.fields.TextField')(max_length=4000)),
        ))
        db.send_create_signal(u'boe_analisis', ['Referencia'])

        # Adding unique constraint on 'Referencia', fields ['referencia', 'palabra']
        db.create_unique(u'boe_analisis_referencia', ['referencia_id', 'palabra_id'])

        # Adding model 'Documento'
        db.create_table(u'boe_analisis_documento', (
            ('identificador', self.gf('django.db.models.fields.CharField')(max_length=25, primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('diario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['boe_analisis.Diario'], null=True)),
            ('diario_numero', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('seccion', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('subseccion', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('rango', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['boe_analisis.Rango'], null=True)),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['boe_analisis.Departamento'], null=True)),
            ('numero_oficial', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('fecha_disposicion', self.gf('django.db.models.fields.DateField')(null=True)),
            ('fecha_publicacion', self.gf('django.db.models.fields.DateField')(null=True)),
            ('fecha_vigencia', self.gf('django.db.models.fields.DateField')(null=True)),
            ('fecha_derogacion', self.gf('django.db.models.fields.DateField')(null=True)),
            ('letra_imagen', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('pagina_inicial', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('pagina_final', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('suplemento_letra_imagen', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('suplemento_pagina_inicial', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('suplemento_pagina_final', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('estatus_legislativo', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('origen_legislativo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['boe_analisis.Origen_legislativo'], null=True)),
            ('estado_consolidacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['boe_analisis.Estado_consolidacion'], null=True)),
            ('judicialmente_anulada', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('vigencia_agotada', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('url_epub', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('url_xml', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('url_htm', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('url_pdf', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('url_pdf_catalan', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('url_pdf_euskera', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('url_pdf_gallego', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('url_pdf_valenciano', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('texto', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'boe_analisis', ['Documento'])

        # Adding M2M table for field notas on 'Documento'
        m2m_table_name = db.shorten_name(u'boe_analisis_documento_notas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('documento', models.ForeignKey(orm[u'boe_analisis.documento'], null=False)),
            ('nota', models.ForeignKey(orm[u'boe_analisis.nota'], null=False))
        ))
        db.create_unique(m2m_table_name, ['documento_id', 'nota_id'])

        # Adding M2M table for field materias on 'Documento'
        m2m_table_name = db.shorten_name(u'boe_analisis_documento_materias')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('documento', models.ForeignKey(orm[u'boe_analisis.documento'], null=False)),
            ('materia', models.ForeignKey(orm[u'boe_analisis.materia'], null=False))
        ))
        db.create_unique(m2m_table_name, ['documento_id', 'materia_id'])

        # Adding M2M table for field alertas on 'Documento'
        m2m_table_name = db.shorten_name(u'boe_analisis_documento_alertas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('documento', models.ForeignKey(orm[u'boe_analisis.documento'], null=False)),
            ('alerta', models.ForeignKey(orm[u'boe_analisis.alerta'], null=False))
        ))
        db.create_unique(m2m_table_name, ['documento_id', 'alerta_id'])

        # Adding M2M table for field referencias_anteriores on 'Documento'
        m2m_table_name = db.shorten_name(u'boe_analisis_documento_referencias_anteriores')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('documento', models.ForeignKey(orm[u'boe_analisis.documento'], null=False)),
            ('referencia', models.ForeignKey(orm[u'boe_analisis.referencia'], null=False))
        ))
        db.create_unique(m2m_table_name, ['documento_id', 'referencia_id'])

        # Adding M2M table for field referencias_posteriores on 'Documento'
        m2m_table_name = db.shorten_name(u'boe_analisis_documento_referencias_posteriores')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('documento', models.ForeignKey(orm[u'boe_analisis.documento'], null=False)),
            ('referencia', models.ForeignKey(orm[u'boe_analisis.referencia'], null=False))
        ))
        db.create_unique(m2m_table_name, ['documento_id', 'referencia_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Referencia', fields ['referencia', 'palabra']
        db.delete_unique(u'boe_analisis_referencia', ['referencia_id', 'palabra_id'])

        # Removing unique constraint on 'Nota', fields ['codigo', 'titulo']
        db.delete_unique(u'boe_analisis_nota', ['codigo', 'titulo'])

        # Deleting model 'Diario'
        db.delete_table(u'boe_analisis_diario')

        # Deleting model 'Departamento'
        db.delete_table(u'boe_analisis_departamento')

        # Deleting model 'Rango'
        db.delete_table(u'boe_analisis_rango')

        # Deleting model 'Origen_legislativo'
        db.delete_table(u'boe_analisis_origen_legislativo')

        # Deleting model 'Estado_consolidacion'
        db.delete_table(u'boe_analisis_estado_consolidacion')

        # Deleting model 'Nota'
        db.delete_table(u'boe_analisis_nota')

        # Deleting model 'Materia'
        db.delete_table(u'boe_analisis_materia')

        # Deleting model 'Alerta'
        db.delete_table(u'boe_analisis_alerta')

        # Deleting model 'Palabra'
        db.delete_table(u'boe_analisis_palabra')

        # Deleting model 'Referencia'
        db.delete_table(u'boe_analisis_referencia')

        # Deleting model 'Documento'
        db.delete_table(u'boe_analisis_documento')

        # Removing M2M table for field notas on 'Documento'
        db.delete_table(db.shorten_name(u'boe_analisis_documento_notas'))

        # Removing M2M table for field materias on 'Documento'
        db.delete_table(db.shorten_name(u'boe_analisis_documento_materias'))

        # Removing M2M table for field alertas on 'Documento'
        db.delete_table(db.shorten_name(u'boe_analisis_documento_alertas'))

        # Removing M2M table for field referencias_anteriores on 'Documento'
        db.delete_table(db.shorten_name(u'boe_analisis_documento_referencias_anteriores'))

        # Removing M2M table for field referencias_posteriores on 'Documento'
        db.delete_table(db.shorten_name(u'boe_analisis_documento_referencias_posteriores'))


    models = {
        u'boe_analisis.alerta': {
            'Meta': {'object_name': 'Alerta'},
            'codigo': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'boe_analisis.departamento': {
            'Meta': {'object_name': 'Departamento'},
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'boe_analisis.diario': {
            'Meta': {'object_name': 'Diario'},
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'boe_analisis.materia': {
            'Meta': {'object_name': 'Materia'},
            'codigo': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'boe_analisis.nota': {
            'Meta': {'unique_together': "(('codigo', 'titulo'),)", 'object_name': 'Nota'},
            'codigo': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'boe_analisis.origen_legislativo': {
            'Meta': {'object_name': 'Origen_legislativo'},
            'codigo': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'boe_analisis.palabra': {
            'Meta': {'object_name': 'Palabra'},
            'codigo': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'boe_analisis.rango': {
            'Meta': {'object_name': 'Rango'},
            'codigo': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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