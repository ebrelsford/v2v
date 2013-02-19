# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'ViolationLocation', fields ['external_id']
        db.create_unique(u'violations_violationlocation', ['external_id'])


        # Changing field 'ViolationType.full_description'
        db.alter_column(u'violations_violationtype', 'full_description', self.gf('django.db.models.fields.TextField')(null=True))
        # Adding unique constraint on 'ViolationType', fields ['code']
        db.create_unique(u'violations_violationtype', ['code'])

        # Deleting field 'Violation.datetime'
        db.delete_column(u'violations_violation', 'datetime')

        # Adding field 'Violation.violation_datetime'
        db.add_column(u'violations_violation', 'violation_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'Violation', fields ['external_id']
        db.create_unique(u'violations_violation', ['external_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Violation', fields ['external_id']
        db.delete_unique(u'violations_violation', ['external_id'])

        # Removing unique constraint on 'ViolationType', fields ['code']
        db.delete_unique(u'violations_violationtype', ['code'])

        # Removing unique constraint on 'ViolationLocation', fields ['external_id']
        db.delete_unique(u'violations_violationlocation', ['external_id'])


        # User chose to not deal with backwards NULL issues for 'ViolationType.full_description'
        raise RuntimeError("Cannot reverse this migration. 'ViolationType.full_description' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Violation.datetime'
        raise RuntimeError("Cannot reverse this migration. 'Violation.datetime' and its values cannot be restored.")
        # Deleting field 'Violation.violation_datetime'
        db.delete_column(u'violations_violation', 'violation_datetime')


    models = {
        u'violations.violation': {
            'Meta': {'object_name': 'Violation'},
            'external_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'violation_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'violation_location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['violations.ViolationLocation']"}),
            'violation_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['violations.ViolationType']"})
        },
        u'violations.violationlocation': {
            'Meta': {'object_name': 'ViolationLocation'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'violations.violationtype': {
            'Meta': {'object_name': 'ViolationType'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'full_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'li_description': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['violations']