# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Lot.water_parcel'
        db.add_column(u'lots_lot', 'water_parcel',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['waterdept.WaterParcel'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Lot.water_parcel'
        db.delete_column(u'lots_lot', 'water_parcel_id')


    models = {
        u'availableproperties.availableproperty': {
            'Meta': {'object_name': 'AvailableProperty'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'agency': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'asset_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {}),
            'mapreg': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'price_str': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new and available'", 'max_length': '30'})
        },
        u'lots.lot': {
            'Meta': {'object_name': 'Lot'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'address_line1': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'available_property': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['availableproperties.AvailableProperty']", 'null': 'True', 'blank': 'True'}),
            'billing_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opa.BillingAccount']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['owners.Owner']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'parcel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parcels.Parcel']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'polygon': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'violations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['violations.Violation']", 'null': 'True', 'blank': 'True'}),
            'water_parcel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['waterdept.WaterParcel']", 'null': 'True', 'blank': 'True'})
        },
        u'opa.accountowner': {
            'Meta': {'object_name': 'AccountOwner'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['owners.Owner']", 'null': 'True', 'blank': 'True'})
        },
        u'opa.billingaccount': {
            'Meta': {'object_name': 'BillingAccount'},
            'account_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opa.AccountOwner']", 'null': 'True', 'blank': 'True'}),
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
            'agency_codes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['owners.AgencyCode']", 'null': 'True', 'blank': 'True'}),
            'aliases': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['owners.Alias']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'owner_type': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '20'})
        },
        u'parcels.parcel': {
            'Meta': {'object_name': 'Parcel'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'basereg': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapreg': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'stcod': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
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

    complete_apps = ['lots']