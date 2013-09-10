# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ProjectSettings.logo_font'
        db.add_column(u'settings_projectsettings', 'logo_font',
                      self.gf('django.db.models.fields.files.FileField')(default=2, max_length=100),
                      keep_default=False)

        # Adding field 'ProjectSettings.logo'
        db.add_column(u'settings_projectsettings', 'logo',
                      self.gf('django.db.models.fields.files.ImageField')(default=2, max_length=100, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ProjectSettings.logo_font'
        db.delete_column(u'settings_projectsettings', 'logo_font')

        # Deleting field 'ProjectSettings.logo'
        db.delete_column(u'settings_projectsettings', 'logo')


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
            'invoice_address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'invoice_country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'invoice_cp': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'invoice_town': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'logo_font': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'registration_open': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tax_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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