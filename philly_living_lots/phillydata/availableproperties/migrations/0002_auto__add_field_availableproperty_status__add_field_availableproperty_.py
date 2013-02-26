# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'AvailableProperty.status'
        db.add_column(u'availableproperties_availableproperty', 'status',
                      self.gf('django.db.models.fields.CharField')(default='new and available', max_length=30),
                      keep_default=False)

        # Adding field 'AvailableProperty.added'
        db.add_column(u'availableproperties_availableproperty', 'added',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 2, 25, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'AvailableProperty.last_seen'
        db.add_column(u'availableproperties_availableproperty', 'last_seen',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 2, 25, 0, 0)),
                      keep_default=False)

        # Adding unique constraint on 'AvailableProperty', fields ['asset_id']
        db.create_unique(u'availableproperties_availableproperty', ['asset_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'AvailableProperty', fields ['asset_id']
        db.delete_unique(u'availableproperties_availableproperty', ['asset_id'])

        # Deleting field 'AvailableProperty.status'
        db.delete_column(u'availableproperties_availableproperty', 'status')

        # Deleting field 'AvailableProperty.added'
        db.delete_column(u'availableproperties_availableproperty', 'added')

        # Deleting field 'AvailableProperty.last_seen'
        db.delete_column(u'availableproperties_availableproperty', 'last_seen')


    models = {
        u'availableproperties.availableproperty': {
            'Meta': {'object_name': 'AvailableProperty'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'agency': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'asset_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {}),
            'mapreg': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'price_str': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new and available'", 'max_length': '30'})
        }
    }

    complete_apps = ['availableproperties']