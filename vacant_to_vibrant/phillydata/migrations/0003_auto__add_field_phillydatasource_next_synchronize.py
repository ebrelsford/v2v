# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PhillyDataSource.next_synchronize'
        db.add_column(u'phillydata_phillydatasource', 'next_synchronize',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 31, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PhillyDataSource.next_synchronize'
        db.delete_column(u'phillydata_phillydatasource', 'next_synchronize')


    models = {
        u'phillydata.phillydatasource': {
            'Meta': {'object_name': 'PhillyDataSource'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'healthy': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_synchronized': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'next_synchronize': ('django.db.models.fields.DateTimeField', [], {}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['phillydata']