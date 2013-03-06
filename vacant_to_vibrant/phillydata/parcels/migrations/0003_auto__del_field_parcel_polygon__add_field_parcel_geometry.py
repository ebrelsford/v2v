# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Parcel.polygon'
        db.delete_column(u'parcels_parcel', 'polygon')

        # Adding field 'Parcel.geometry'
        db.add_column(u'parcels_parcel', 'geometry',
                      self.gf('django.contrib.gis.db.models.fields.GeometryField')(default=None),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Parcel.polygon'
        raise RuntimeError("Cannot reverse this migration. 'Parcel.polygon' and its values cannot be restored.")
        # Deleting field 'Parcel.geometry'
        db.delete_column(u'parcels_parcel', 'geometry')


    models = {
        u'parcels.parcel': {
            'Meta': {'object_name': 'Parcel'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'basereg': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapreg': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'stcod': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['parcels']