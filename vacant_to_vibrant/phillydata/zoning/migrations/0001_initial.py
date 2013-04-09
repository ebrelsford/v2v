# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BaseDistrict'
        db.create_table(u'zoning_basedistrict', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
            ('zoning_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoning.ZoningType'])),
        ))
        db.send_create_signal(u'zoning', ['BaseDistrict'])

        # Adding model 'ZoningType'
        db.create_table(u'zoning_zoningtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('long_code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'zoning', ['ZoningType'])


    def backwards(self, orm):
        # Deleting model 'BaseDistrict'
        db.delete_table(u'zoning_basedistrict')

        # Deleting model 'ZoningType'
        db.delete_table(u'zoning_zoningtype')


    models = {
        u'zoning.basedistrict': {
            'Meta': {'object_name': 'BaseDistrict'},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zoning_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zoning.ZoningType']"})
        },
        u'zoning.zoningtype': {
            'Meta': {'object_name': 'ZoningType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_code': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['zoning']