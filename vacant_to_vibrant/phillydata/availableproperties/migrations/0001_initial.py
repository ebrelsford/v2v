# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AvailableProperty'
        db.create_table(u'availableproperties_availableproperty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('centroid', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('asset_id', self.gf('django.db.models.fields.CharField')(max_length=10, unique=True, null=True, blank=True)),
            ('mapreg', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('agency', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2, blank=True)),
            ('price_str', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('area', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='new and available', max_length=30)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_seen', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'availableproperties', ['AvailableProperty'])


    def backwards(self, orm):
        # Deleting model 'AvailableProperty'
        db.delete_table(u'availableproperties_availableproperty')


    models = {
        u'availableproperties.availableproperty': {
            'Meta': {'object_name': 'AvailableProperty'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'agency': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'asset_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {}),
            'mapreg': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'price_str': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new and available'", 'max_length': '30'})
        }
    }

    complete_apps = ['availableproperties']