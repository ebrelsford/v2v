# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lot'
        db.create_table(u'lots_lot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('centroid', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True)),
            ('polygon', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('address_line1', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('address_line2', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('state_province', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('parcel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parcels.Parcel'], null=True, blank=True)),
        ))
        db.send_create_signal(u'lots', ['Lot'])

        # Adding M2M table for field violations on 'Lot'
        db.create_table(u'lots_lot_violations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lot', models.ForeignKey(orm[u'lots.lot'], null=False)),
            ('violation', models.ForeignKey(orm[u'violations.violation'], null=False))
        ))
        db.create_unique(u'lots_lot_violations', ['lot_id', 'violation_id'])


    def backwards(self, orm):
        # Deleting model 'Lot'
        db.delete_table(u'lots_lot')

        # Removing M2M table for field violations on 'Lot'
        db.delete_table('lots_lot_violations')


    models = {
        u'lots.lot': {
            'Meta': {'object_name': 'Lot'},
            'address_line1': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'parcel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parcels.Parcel']", 'null': 'True', 'blank': 'True'}),
            'polygon': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'violations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['violations.Violation']", 'null': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['lots']