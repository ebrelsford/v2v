# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BillingAccount.improvement_description'
        db.add_column(u'owners_billingaccount', 'improvement_description',
                      self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BillingAccount.sale_date'
        db.add_column(u'owners_billingaccount', 'sale_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BillingAccount.land_area'
        db.add_column(u'owners_billingaccount', 'land_area',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BillingAccount.improvement_area'
        db.add_column(u'owners_billingaccount', 'improvement_area',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BillingAccount.assessment'
        db.add_column(u'owners_billingaccount', 'assessment',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'BillingAccount.last_updated'
        db.add_column(u'owners_billingaccount', 'last_updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 2, 18, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'BillingAccount.improvement_description'
        db.delete_column(u'owners_billingaccount', 'improvement_description')

        # Deleting field 'BillingAccount.sale_date'
        db.delete_column(u'owners_billingaccount', 'sale_date')

        # Deleting field 'BillingAccount.land_area'
        db.delete_column(u'owners_billingaccount', 'land_area')

        # Deleting field 'BillingAccount.improvement_area'
        db.delete_column(u'owners_billingaccount', 'improvement_area')

        # Deleting field 'BillingAccount.assessment'
        db.delete_column(u'owners_billingaccount', 'assessment')

        # Deleting field 'BillingAccount.last_updated'
        db.delete_column(u'owners_billingaccount', 'last_updated')


    models = {
        u'owners.billingaccount': {
            'Meta': {'object_name': 'BillingAccount'},
            'assessment': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'improvement_area': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'improvement_description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'land_area': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'mailing_address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'mailing_city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'mailing_country': ('django.db.models.fields.CharField', [], {'default': "'USA'", 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'mailing_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'mailing_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'mailing_state_province': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'property_address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'sale_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'owners.owner': {
            'Meta': {'object_name': 'Owner'},
            'billing_accounts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['owners.BillingAccount']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        }
    }

    complete_apps = ['owners']