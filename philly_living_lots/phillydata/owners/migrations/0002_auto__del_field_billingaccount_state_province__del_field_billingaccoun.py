# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'BillingAccount.state_province'
        db.delete_column(u'owners_billingaccount', 'state_province')

        # Deleting field 'BillingAccount.city'
        db.delete_column(u'owners_billingaccount', 'city')

        # Deleting field 'BillingAccount.postal_code'
        db.delete_column(u'owners_billingaccount', 'postal_code')

        # Deleting field 'BillingAccount.street_address'
        db.delete_column(u'owners_billingaccount', 'street_address')

        # Adding field 'BillingAccount.property_address'
        db.add_column(u'owners_billingaccount', 'property_address',
                      self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BillingAccount.mailing_address'
        db.add_column(u'owners_billingaccount', 'mailing_address',
                      self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BillingAccount.mailing_postal_code'
        db.add_column(u'owners_billingaccount', 'mailing_postal_code',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BillingAccount.mailing_city'
        db.add_column(u'owners_billingaccount', 'mailing_city',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BillingAccount.mailing_state_province'
        db.add_column(u'owners_billingaccount', 'mailing_state_province',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'BillingAccount.state_province'
        db.add_column(u'owners_billingaccount', 'state_province',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BillingAccount.city'
        db.add_column(u'owners_billingaccount', 'city',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BillingAccount.postal_code'
        db.add_column(u'owners_billingaccount', 'postal_code',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BillingAccount.street_address'
        db.add_column(u'owners_billingaccount', 'street_address',
                      self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'BillingAccount.property_address'
        db.delete_column(u'owners_billingaccount', 'property_address')

        # Deleting field 'BillingAccount.mailing_address'
        db.delete_column(u'owners_billingaccount', 'mailing_address')

        # Deleting field 'BillingAccount.mailing_postal_code'
        db.delete_column(u'owners_billingaccount', 'mailing_postal_code')

        # Deleting field 'BillingAccount.mailing_city'
        db.delete_column(u'owners_billingaccount', 'mailing_city')

        # Deleting field 'BillingAccount.mailing_state_province'
        db.delete_column(u'owners_billingaccount', 'mailing_state_province')


    models = {
        u'owners.billingaccount': {
            'Meta': {'object_name': 'BillingAccount'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailing_address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'mailing_city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'mailing_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'mailing_state_province': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'property_address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        u'owners.owner': {
            'Meta': {'object_name': 'Owner'},
            'billing_accounts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['owners.BillingAccount']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['owners']