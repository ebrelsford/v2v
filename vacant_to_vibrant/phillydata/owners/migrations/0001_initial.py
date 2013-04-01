# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Alias'
        db.create_table(u'owners_alias', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
        ))
        db.send_create_signal(u'owners', ['Alias'])

        # Adding model 'Owner'
        db.create_table(u'owners_owner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('owner_type', self.gf('django.db.models.fields.CharField')(default='unknown', max_length=20)),
        ))
        db.send_create_signal(u'owners', ['Owner'])

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

        # Adding model 'AgencyCode'
        db.create_table(u'owners_agencycode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
        ))
        db.send_create_signal(u'owners', ['AgencyCode'])


    def backwards(self, orm):
        # Deleting model 'Alias'
        db.delete_table(u'owners_alias')

        # Deleting model 'Owner'
        db.delete_table(u'owners_owner')

        # Removing M2M table for field aliases on 'Owner'
        db.delete_table('owners_owner_aliases')

        # Removing M2M table for field agency_codes on 'Owner'
        db.delete_table('owners_owner_agency_codes')

        # Deleting model 'AgencyCode'
        db.delete_table(u'owners_agencycode')


    models = {
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
        }
    }

    complete_apps = ['owners']