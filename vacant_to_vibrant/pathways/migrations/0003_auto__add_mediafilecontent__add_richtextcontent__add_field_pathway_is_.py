# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MediaFileContent'
        db.create_table(u'pathways_pathway_mediafilecontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mediafile', self.gf('feincms.module.medialibrary.fields.MediaFileForeignKey')(related_name='+', to=orm['medialibrary.MediaFile'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mediafilecontent_set', to=orm['pathways.Pathway'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('type', self.gf('django.db.models.fields.CharField')(default='default', max_length=20)),
        ))
        db.send_create_signal(u'pathways', ['MediaFileContent'])

        # Adding model 'RichTextContent'
        db.create_table(u'pathways_pathway_richtextcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('feincms.contrib.richtext.RichTextField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='richtextcontent_set', to=orm['pathways.Pathway'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'pathways', ['RichTextContent'])

        # Adding field 'Pathway.is_active'
        db.add_column(u'pathways_pathway', 'is_active',
                      self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True),
                      keep_default=False)

        # Adding field 'Pathway.publication_date'
        db.add_column(u'pathways_pathway', 'publication_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 15, 0, 0)),
                      keep_default=False)

        # Adding field 'Pathway.publication_end_date'
        db.add_column(u'pathways_pathway', 'publication_end_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Pathway.language'
        db.add_column(u'pathways_pathway', 'language',
                      self.gf('django.db.models.fields.CharField')(default='en', max_length=10),
                      keep_default=False)

        # Adding field 'Pathway.translation_of'
        db.add_column(u'pathways_pathway', 'translation_of',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='translations', null=True, to=orm['pathways.Pathway']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'MediaFileContent'
        db.delete_table(u'pathways_pathway_mediafilecontent')

        # Deleting model 'RichTextContent'
        db.delete_table(u'pathways_pathway_richtextcontent')

        # Deleting field 'Pathway.is_active'
        db.delete_column(u'pathways_pathway', 'is_active')

        # Deleting field 'Pathway.publication_date'
        db.delete_column(u'pathways_pathway', 'publication_date')

        # Deleting field 'Pathway.publication_end_date'
        db.delete_column(u'pathways_pathway', 'publication_end_date')

        # Deleting field 'Pathway.language'
        db.delete_column(u'pathways_pathway', 'language')

        # Deleting field 'Pathway.translation_of'
        db.delete_column(u'pathways_pathway', 'translation_of_id')


    models = {
        u'medialibrary.category': {
            'Meta': {'ordering': "['parent__title', 'title']", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['medialibrary.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'medialibrary.mediafile': {
            'Meta': {'ordering': "['-created']", 'object_name': 'MediaFile'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['medialibrary.Category']", 'null': 'True', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        u'pathways.mediafilecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'MediaFileContent', 'db_table': "u'pathways_pathway_mediafilecontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mediafile': ('feincms.module.medialibrary.fields.MediaFileForeignKey', [], {'related_name': "'+'", 'to': u"orm['medialibrary.MediaFile']"}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mediafilecontent_set'", 'to': u"orm['pathways.Pathway']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '20'})
        },
        u'pathways.pathway': {
            'Meta': {'object_name': 'Pathway'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 15, 0, 0)'}),
            'publication_end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'translation_of': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'translations'", 'null': 'True', 'to': u"orm['pathways.Pathway']"})
        },
        u'pathways.richtextcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'RichTextContent', 'db_table': "u'pathways_pathway_richtextcontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'richtextcontent_set'", 'to': u"orm['pathways.Pathway']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('feincms.contrib.richtext.RichTextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['pathways']