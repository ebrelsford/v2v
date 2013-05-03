# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CityCouncilMember.district'
        db.alter_column(u'citycouncil_citycouncilmember', 'district_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['boundaries.Boundary'], null=True, on_delete=models.SET_NULL))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'CityCouncilMember.district'
        raise RuntimeError("Cannot reverse this migration. 'CityCouncilMember.district' and its values cannot be restored.")

    models = {
        u'boundaries.boundary': {
            'Meta': {'ordering': "('layer__name', 'label')", 'object_name': 'Boundary'},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'layer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boundaries.Layer']"})
        },
        u'boundaries.layer': {
            'Meta': {'object_name': 'Layer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'source_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'citycouncil.citycouncilmember': {
            'Meta': {'object_name': 'CityCouncilMember'},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boundaries.Boundary']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['citycouncil']