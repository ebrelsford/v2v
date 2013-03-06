# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AgencyCode'
        db.create_table(u'owners_agencycode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
        ))
        db.send_create_signal(u'owners', ['AgencyCode'])

        # Adding model 'Alias'
        db.create_table(u'owners_alias', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
        ))
        db.send_create_signal(u'owners', ['Alias'])

        # Adding field 'Owner.owner_type'
        db.add_column(u'owners_owner', 'owner_type',
                      self.gf('django.db.models.fields.CharField')(default='public', max_length=20),
                      keep_default=False)

        # Adding M2M table for field aliases on 'Owner'
        db.create_table(u'owners_owner_aliases', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('owner', models.ForeignKey(orm[u'owners.owner'], null=False)),
            ('alias', models.ForeignKey(orm[u'owners.alias'], null=False))
        ))
        db.create_unique(u'owners_owner_aliases', ['owner_id', 'alias_id'])

        # Adding M2M table for field agency_codes on 'Owner'
        db.create_table(u'owners_owner_agency_codes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('owner', models.ForeignKey(orm[u'owners.owner'], null=False)),
            ('agencycode', models.ForeignKey(orm[u'owners.agencycode'], null=False))
        ))
        db.create_unique(u'owners_owner_agency_codes', ['owner_id', 'agencycode_id'])

        # Adding M2M table for field account_owners on 'Owner'
        db.create_table(u'owners_owner_account_owners', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('owner', models.ForeignKey(orm[u'owners.owner'], null=False)),
            ('accountowner', models.ForeignKey(orm[u'opa.accountowner'], null=False))
        ))
        db.create_unique(u'owners_owner_account_owners', ['owner_id', 'accountowner_id'])


    def backwards(self, orm):
        # Deleting model 'AgencyCode'
        db.delete_table(u'owners_agencycode')

        # Deleting model 'Alias'
        db.delete_table(u'owners_alias')

        # Deleting field 'Owner.owner_type'
        db.delete_column(u'owners_owner', 'owner_type')

        # Removing M2M table for field aliases on 'Owner'
        db.delete_table('owners_owner_aliases')

        # Removing M2M table for field agency_codes on 'Owner'
        db.delete_table('owners_owner_agency_codes')

        # Removing M2M table for field account_owners on 'Owner'
        db.delete_table('owners_owner_account_owners')


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
        },
        u'owners.agencycode': {
            'Meta': {'object_name': 'AgencyCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'owners.alias': {
            'Meta': {'object_name': 'Alias'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        u'owners.owner': {
            'Meta': {'object_name': 'Owner'},
            'account_owners': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['opa.AccountOwner']", 'symmetrical': 'False'}),
            'agency_codes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['owners.AgencyCode']", 'symmetrical': 'False'}),
            'aliases': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['owners.Alias']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'owner_type': ('django.db.models.fields.CharField', [], {'default': "'public'", 'max_length': '20'})
        }
    }

    complete_apps = ['owners']