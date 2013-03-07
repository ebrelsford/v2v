# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LandUseArea'
        db.create_table(u'landuse_landusearea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
            ('object_id', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('subcategory', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('vacant_building', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'landuse', ['LandUseArea'])


    def backwards(self, orm):
        # Deleting model 'LandUseArea'
        db.delete_table(u'landuse_landusearea')


    models = {
        u'landuse.landusearea': {
            'Meta': {'object_name': 'LandUseArea'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'subcategory': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'vacant_building': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['landuse']