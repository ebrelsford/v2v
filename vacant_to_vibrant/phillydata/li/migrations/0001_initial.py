# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'li_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('external_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal(u'li', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'li_location')


    models = {
        u'li.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['li']