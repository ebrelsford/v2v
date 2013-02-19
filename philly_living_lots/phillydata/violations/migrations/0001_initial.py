# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Violation'
        db.create_table(u'violations_violation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('violation_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['violations.ViolationType'])),
            ('violation_location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['violations.ViolationLocation'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'violations', ['Violation'])

        # Adding model 'ViolationType'
        db.create_table(u'violations_violationtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('li_description', self.gf('django.db.models.fields.TextField')()),
            ('full_description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'violations', ['ViolationType'])

        # Adding model 'ViolationLocation'
        db.create_table(u'violations_violationlocation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'violations', ['ViolationLocation'])


    def backwards(self, orm):
        # Deleting model 'Violation'
        db.delete_table(u'violations_violation')

        # Deleting model 'ViolationType'
        db.delete_table(u'violations_violationtype')

        # Deleting model 'ViolationLocation'
        db.delete_table(u'violations_violationlocation')


    models = {
        u'violations.violation': {
            'Meta': {'object_name': 'Violation'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'violation_location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['violations.ViolationLocation']"}),
            'violation_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['violations.ViolationType']"})
        },
        u'violations.violationlocation': {
            'Meta': {'object_name': 'ViolationLocation'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'violations.violationtype': {
            'Meta': {'object_name': 'ViolationType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'full_description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'li_description': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['violations']