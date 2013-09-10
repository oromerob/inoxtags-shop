# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HomeSlider'
        db.create_table(u'content_pages_homeslider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('ckeditor.fields.RichTextField')()),
            ('btn_link', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('btn_txt', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'content_pages', ['HomeSlider'])

        # Adding model 'HomeFeaturette'
        db.create_table(u'content_pages_homefeaturette', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slogan', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('subslogan', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('ckeditor.fields.RichTextField')()),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('img_desc', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'content_pages', ['HomeFeaturette'])


    def backwards(self, orm):
        # Deleting model 'HomeSlider'
        db.delete_table(u'content_pages_homeslider')

        # Deleting model 'HomeFeaturette'
        db.delete_table(u'content_pages_homefeaturette')


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
            'text': ('ckeditor.fields.RichTextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['content_pages']