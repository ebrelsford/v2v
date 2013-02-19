# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'BillingAccount.country'
        db.delete_column(u'owners_billingaccount', 'country')

        # Adding field 'BillingAccount.mailing_country'
        db.add_column(u'owners_billingaccount', 'mailing_country',
                      self.gf('django.db.models.fields.CharField')(default='USA', max_length=40, null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'BillingAccount', fields ['external_id']
        db.create_unique(u'owners_billingaccount', ['external_id'])

        # Adding unique constraint on 'Owner', fields ['name']
        db.create_unique(u'owners_owner', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Owner', fields ['name']
        db.delete_unique(u'owners_owner', ['name'])

        # Removing unique constraint on 'BillingAccount', fields ['external_id']
        db.delete_unique(u'owners_billingaccount', ['external_id'])

        # Adding field 'BillingAccount.country'
        db.add_column(u'owners_billingaccount', 'country',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'BillingAccount.mailing_country'
        db.delete_column(u'owners_billingaccount', 'mailing_country')


    models = {
        u'owners.billingaccount': {
            'Meta': {'object_name': 'BillingAccount'},
            'external_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailing_address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'mailing_city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'mailing_country': ('django.db.models.fields.CharField', [], {'default': "'USA'", 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'mailing_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'mailing_state_province': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'property_address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        u'owners.owner': {
            'Meta': {'object_name': 'Owner'},
            'billing_accounts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['owners.BillingAccount']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        }
    }

    complete_apps = ['owners']