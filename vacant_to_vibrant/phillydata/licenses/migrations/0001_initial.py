# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'License'
        db.create_table(u'licenses_license', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('license_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licenses.LicenseType'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['li.Location'])),
            ('primary_contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['licenses.Contact'], null=True, blank=True)),
            ('issued_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('inactive_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('external_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('expires_month', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('expires_year', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal(u'licenses', ['License'])

        # Adding model 'LicenseType'
        db.create_table(u'licenses_licensetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'licenses', ['LicenseType'])

        # Adding model 'Contact'
        db.create_table(u'licenses_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact_type', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'licenses', ['Contact'])


    def backwards(self, orm):
        # Deleting model 'License'
        db.delete_table(u'licenses_license')

        # Deleting model 'LicenseType'
        db.delete_table(u'licenses_licensetype')

        # Deleting model 'Contact'
        db.delete_table(u'licenses_contact')


    models = {
        u'li.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'licenses.contact': {
            'Meta': {'object_name': 'Contact'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'contact_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'licenses.license': {
            'Meta': {'object_name': 'License'},
            'expires_month': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'expires_year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inactive_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'issued_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'license_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licenses.LicenseType']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['li.Location']"}),
            'primary_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['licenses.Contact']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        u'licenses.licensetype': {
            'Meta': {'object_name': 'LicenseType'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['licenses']