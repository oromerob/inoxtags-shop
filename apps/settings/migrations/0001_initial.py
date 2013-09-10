# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProjectSettings'
        db.create_table(u'settings_projectsettings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('registration_open', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'settings', ['ProjectSettings'])

        # Adding model 'Tag'
        db.create_table(u'settings_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'settings', ['Tag'])

        # Adding model 'Tos'
        db.create_table(u'settings_tos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('terms', self.gf('ckeditor.fields.RichTextField')()),
            ('privacity', self.gf('ckeditor.fields.RichTextField')()),
        ))
        db.send_create_signal(u'settings', ['Tos'])


    def backwards(self, orm):
        # Deleting model 'ProjectSettings'
        db.delete_table(u'settings_projectsettings')

        # Deleting model 'Tag'
        db.delete_table(u'settings_tag')

        # Deleting model 'Tos'
        db.delete_table(u'settings_tos')


    models = {
        u'settings.projectsettings': {
            'Meta': {'object_name': 'ProjectSettings'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'registration_open': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'settings.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'settings.tos': {
            'Meta': {'object_name': 'Tos'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'privacity': ('ckeditor.fields.RichTextField', [], {}),
            'terms': ('ckeditor.fields.RichTextField', [], {})
        }
    }

    complete_apps = ['settings']