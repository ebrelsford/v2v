# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AccountOwner'
        db.create_table(u'opa_accountowner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
        ))
        db.send_create_signal(u'opa', ['AccountOwner'])

        # Adding M2M table for field billing_accounts on 'AccountOwner'
        db.create_table(u'opa_accountowner_billing_accounts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('accountowner', models.ForeignKey(orm[u'opa.accountowner'], null=False)),
            ('billingaccount', models.ForeignKey(orm[u'opa.billingaccount'], null=False))
        ))
        db.create_unique(u'opa_accountowner_billing_accounts', ['accountowner_id', 'billingaccount_id'])

        # Adding model 'BillingAccount'
        db.create_table(u'opa_billingaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('external_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('property_address', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('improvement_description', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('sale_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('land_area', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=3, blank=True)),
            ('improvement_area', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=2, blank=True)),
            ('mailing_name', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('mailing_address', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('mailing_postal_code', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('mailing_city', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('mailing_state_province', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('mailing_country', self.gf('django.db.models.fields.CharField')(default='USA', max_length=40, null=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'opa', ['BillingAccount'])


    def backwards(self, orm):
        # Deleting model 'AccountOwner'
        db.delete_table(u'opa_accountowner')

        # Removing M2M table for field billing_accounts on 'AccountOwner'
        db.delete_table('opa_accountowner_billing_accounts')

        # Deleting model 'BillingAccount'
        db.delete_table(u'opa_billingaccount')


    models = {
        u'opa.accountowner': {
            'Meta': {'object_name': 'AccountOwner'},
            'billing_accounts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['opa.BillingAccount']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        u'opa.billingaccount': {
            'Meta': {'object_name': 'BillingAccount'},
            'assessment': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'improvement_area': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'improvement_description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'land_area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'mailing_address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'mailing_city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'mailing_country': ('django.db.models.fields.CharField', [], {'default': "'USA'", 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'mailing_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'mailing_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'mailing_state_province': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'property_address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'sale_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['opa']