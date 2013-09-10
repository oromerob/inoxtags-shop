# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'shop_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=100, populate_from='category', unique_with=())),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('price_special_1', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('price_special_2', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('price_special_3', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('price_special_4', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('has_color', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_front_main', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_front_tel', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_back_1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_back_2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_back_3', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'shop', ['Category'])

        # Adding model 'Shape'
        db.create_table(u'shop_shape', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shape', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'shop', ['Shape'])

        # Adding model 'Color'
        db.create_table(u'shop_color', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'shop', ['Color'])

        # Adding model 'Product'
        db.create_table(u'shop_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Category'])),
            ('shape', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Shape'])),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=100, populate_from='name')),
            ('img_1', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('img_2', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('img_3', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'shop', ['Product'])

        # Adding model 'Cart'
        db.create_table(u'shop_cart', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('checked_out', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'shop', ['Cart'])

        # Adding model 'CustomProduct'
        db.create_table(u'shop_customproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Cart'])),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Product'])),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Color'], null=True, blank=True)),
            ('front_main', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('front_tel', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('back_1', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('back_2', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('back_3', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('price_special_1', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('price_special_2', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('price_special_3', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('price_special_4', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('made', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('repetition', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'shop', ['CustomProduct'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'shop_category')

        # Deleting model 'Shape'
        db.delete_table(u'shop_shape')

        # Deleting model 'Color'
        db.delete_table(u'shop_color')

        # Deleting model 'Product'
        db.delete_table(u'shop_product')

        # Deleting model 'Cart'
        db.delete_table(u'shop_cart')

        # Deleting model 'CustomProduct'
        db.delete_table(u'shop_customproduct')


    models = {
        u'shop.cart': {
            'Meta': {'ordering': "('-creation_date',)", 'object_name': 'Cart'},
            'checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'shop.category': {
            'Meta': {'object_name': 'Category'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'has_back_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_back_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_back_3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_color': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_front_main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_front_tel': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'price_special_1': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'price_special_2': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'price_special_3': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'price_special_4': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '100', 'populate_from': "'category'", 'unique_with': '()'})
        },
        u'shop.color': {
            'Meta': {'object_name': 'Color'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'shop.customproduct': {
            'Meta': {'object_name': 'CustomProduct'},
            'back_1': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'back_2': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'back_3': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Cart']"}),
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Color']", 'null': 'True', 'blank': 'True'}),
            'front_main': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'front_tel': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'made': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'price_special_1': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'price_special_2': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'price_special_3': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'price_special_4': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Product']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'repetition': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'shop.product': {
            'Meta': {'ordering': "['category']", 'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'img_2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'img_3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'shape': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Shape']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '100', 'populate_from': "'name'"})
        },
        u'shop.shape': {
            'Meta': {'object_name': 'Shape'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shape': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['shop']