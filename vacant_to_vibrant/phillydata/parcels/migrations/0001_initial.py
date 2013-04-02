# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Parcel'
        db.create_table(u'parcels_parcel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
            ('basereg', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('mapreg', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('stcod', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
        ))
        db.send_create_signal(u'parcels', ['Parcel'])


    def backwards(self, orm):
        # Deleting model 'Parcel'
        db.delete_table(u'parcels_parcel')


    models = {
        u'parcels.parcel': {
            'Meta': {'object_name': 'Parcel'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'basereg': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapreg': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'stcod': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['parcels']