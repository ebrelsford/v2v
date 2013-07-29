# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PhillyDataSource.synchronizer_record'
        db.add_column(u'phillydata_phillydatasource', 'synchronizer_record',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['external_data_sync.SynchronizerRecord'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PhillyDataSource.synchronizer_record'
        db.delete_column(u'phillydata_phillydatasource', 'synchronizer_record_id')


    models = {
        u'external_data_sync.synchronizerrecord': {
            'Meta': {'object_name': 'SynchronizerRecord'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'synchronizer_class': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'phillydata.phillydatasource': {
            'Meta': {'ordering': "('ordering',)", 'object_name': 'PhillyDataSource'},
            'batch_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'healthy': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_synchronized': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'next_synchronize': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'synchronize_frequency': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'synchronize_in_progress': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'synchronizer_record': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['external_data_sync.SynchronizerRecord']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['phillydata']