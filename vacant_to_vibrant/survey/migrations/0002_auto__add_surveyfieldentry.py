# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SurveyFieldEntry'
        db.create_table(u'survey_surveyfieldentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field_id', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fields', to=orm['survey.SurveyFormEntry'])),
        ))
        db.send_create_signal(u'survey', ['SurveyFieldEntry'])


    def backwards(self, orm):
        # Deleting model 'SurveyFieldEntry'
        db.delete_table(u'survey_surveyfieldentry')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'survey.surveyfieldentry': {
            'Meta': {'object_name': 'SurveyFieldEntry'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': u"orm['survey.SurveyFormEntry']"}),
            'field_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'})
        },
        u'survey.surveyformentry': {
            'Meta': {'object_name': 'SurveyFormEntry'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'entry_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['survey']