# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ProjectSettings.bank_account'
        db.add_column(u'settings_projectsettings', 'bank_account',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=100),
                      keep_default=False)

        # Adding field 'ProjectSettings.bank_iban'
        db.add_column(u'settings_projectsettings', 'bank_iban',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ProjectSettings.bank_account'
        db.delete_column(u'settings_projectsettings', 'bank_account')

        # Deleting field 'ProjectSettings.bank_iban'
        db.delete_column(u'settings_projectsettings', 'bank_iban')


    models = {
        u'settings.projectsettings': {
            'Meta': {'object_name': 'ProjectSettings'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'bank_account': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'bank_iban': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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