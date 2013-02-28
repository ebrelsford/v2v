# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WaterParcel'
        db.create_table(u'waterdept_waterparcel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parcel_id', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('brt_account', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('ten_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('owner1', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('owner2', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('gross_area', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=2, blank=True)),
            ('impervious_area', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=2, blank=True)),
            ('building_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('building_description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('building_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'waterdept', ['WaterParcel'])

        # Adding model 'WaterAccount'
        db.create_table(u'waterdept_wateraccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('water_parcel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['waterdept.WaterParcel'])),
            ('account_id', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('account_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('customer_id', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('customer_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('inst_id', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('account_status', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('account_status_abbreviation', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('meter_size', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('meter_size_abbreviation', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('service_type', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('service_type_label', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('stormwater_status', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal(u'waterdept', ['WaterAccount'])


    def backwards(self, orm):
        # Deleting model 'WaterParcel'
        db.delete_table(u'waterdept_waterparcel')

        # Deleting model 'WaterAccount'
        db.delete_table(u'waterdept_wateraccount')


    models = {
        u'waterdept.wateraccount': {
            'Meta': {'object_name': 'WaterAccount'},
            'account_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'account_status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'account_status_abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'customer_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inst_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'meter_size': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'meter_size_abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'service_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'service_type_label': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'stormwater_status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'water_parcel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['waterdept.WaterParcel']"})
        },
        u'waterdept.waterparcel': {
            'Meta': {'object_name': 'WaterParcel'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'brt_account': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'building_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'building_description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'building_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'gross_area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impervious_area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'}),
            'owner1': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'owner2': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'parcel_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'ten_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['waterdept']