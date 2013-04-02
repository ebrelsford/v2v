# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PhillyDataSource'
        db.create_table(u'phillydata_phillydatasource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('healthy', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('synchronize_in_progress', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('synchronize_frequency', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('next_synchronize', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_synchronized', self.gf('django.db.models.fields.DateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'phillydata', ['PhillyDataSource'])


    def backwards(self, orm):
        # Deleting model 'PhillyDataSource'
        db.delete_table(u'phillydata_phillydatasource')


    models = {
        u'phillydata.phillydatasource': {
            'Meta': {'ordering': "('ordering',)", 'object_name': 'PhillyDataSource'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'healthy': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_synchronized': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'next_synchronize': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'synchronize_frequency': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'synchronize_in_progress': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['phillydata']