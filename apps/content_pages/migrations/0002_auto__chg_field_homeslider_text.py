# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'HomeSlider.text'
        db.alter_column(u'content_pages_homeslider', 'text', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'HomeSlider.text'
        db.alter_column(u'content_pages_homeslider', 'text', self.gf('ckeditor.fields.RichTextField')())

    models = {
        u'content_pages.homefeaturette': {
            'Meta': {'object_name': 'HomeFeaturette'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'img_desc': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slogan': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subslogan': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('ckeditor.fields.RichTextField', [], {})
        },
        u'content_pages.homeslider': {
            'Meta': {'object_name': 'HomeSlider'},
            'btn_link': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'btn_txt': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['content_pages']