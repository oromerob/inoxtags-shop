# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ProjectSettings.tax_code'
        db.add_column(u'settings_projectsettings', 'tax_code',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=100),
                      keep_default=False)

        # Adding field 'ProjectSettings.invoice_address'
        db.add_column(u'settings_projectsettings', 'invoice_address',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=200),
                      keep_default=False)

        # Adding field 'ProjectSettings.invoice_cp'
        db.add_column(u'settings_projectsettings', 'invoice_cp',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=8),
                      keep_default=False)

        # Adding field 'ProjectSettings.invoice_town'
        db.add_column(u'settings_projectsettings', 'invoice_town',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=100),
                      keep_default=False)

        # Adding field 'ProjectSettings.invoice_country'
        db.add_column(u'settings_projectsettings', 'invoice_country',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ProjectSettings.tax_code'
        db.delete_column(u'settings_projectsettings', 'tax_code')

        # Deleting field 'ProjectSettings.invoice_address'
        db.delete_column(u'settings_projectsettings', 'invoice_address')

        # Deleting field 'ProjectSettings.invoice_cp'
        db.delete_column(u'settings_projectsettings', 'invoice_cp')

        # Deleting field 'ProjectSettings.invoice_town'
        db.delete_column(u'settings_projectsettings', 'invoice_town')

        # Deleting field 'ProjectSettings.invoice_country'
        db.delete_column(u'settings_projectsettings', 'invoice_country')


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