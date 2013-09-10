# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ProjectSettings.phone'
        db.add_column(u'settings_projectsettings', 'phone',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=15),
                      keep_default=False)

        # Adding field 'ProjectSettings.email'
        db.add_column(u'settings_projectsettings', 'email',
                      self.gf('django.db.models.fields.EmailField')(default=2, max_length=75),
                      keep_default=False)

        # Adding field 'ProjectSettings.address'
        db.add_column(u'settings_projectsettings', 'address',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=200),
                      keep_default=False)

        # Adding field 'ProjectSettings.cp'
        db.add_column(u'settings_projectsettings', 'cp',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=8),
                      keep_default=False)

        # Adding field 'ProjectSettings.town'
        db.add_column(u'settings_projectsettings', 'town',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=100),
                      keep_default=False)

        # Adding field 'ProjectSettings.country'
        db.add_column(u'settings_projectsettings', 'country',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ProjectSettings.phone'
        db.delete_column(u'settings_projectsettings', 'phone')

        # Deleting field 'ProjectSettings.email'
        db.delete_column(u'settings_projectsettings', 'email')

        # Deleting field 'ProjectSettings.address'
        db.delete_column(u'settings_projectsettings', 'address')

        # Deleting field 'ProjectSettings.cp'
        db.delete_column(u'settings_projectsettings', 'cp')

        # Deleting field 'ProjectSettings.town'
        db.delete_column(u'settings_projectsettings', 'town')

        # Deleting field 'ProjectSettings.country'
        db.delete_column(u'settings_projectsettings', 'country')


    models = {
        u'settings.projectsettings': {
            'Meta': {'object_name': 'ProjectSettings'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cp': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'registration_open': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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