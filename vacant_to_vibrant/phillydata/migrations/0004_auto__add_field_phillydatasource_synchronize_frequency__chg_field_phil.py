# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PhillyDataSource.synchronize_frequency'
        db.add_column(u'phillydata_phillydatasource', 'synchronize_frequency',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'PhillyDataSource.next_synchronize'
        db.alter_column(u'phillydata_phillydatasource', 'next_synchronize', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):
        # Deleting field 'PhillyDataSource.synchronize_frequency'
        db.delete_column(u'phillydata_phillydatasource', 'synchronize_frequency')


        # User chose to not deal with backwards NULL issues for 'PhillyDataSource.next_synchronize'
        raise RuntimeError("Cannot reverse this migration. 'PhillyDataSource.next_synchronize' and its values cannot be restored.")

    models = {
        u'phillydata.phillydatasource': {
            'Meta': {'object_name': 'PhillyDataSource'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'healthy': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_synchronized': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'next_synchronize': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'synchronize_frequency': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['phillydata']