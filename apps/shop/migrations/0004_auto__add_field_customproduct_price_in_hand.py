# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CustomProduct.price_in_hand'
        db.add_column(u'shop_customproduct', 'price_in_hand',
                      self.gf('django.db.models.fields.DecimalField')(default=2, max_digits=5, decimal_places=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CustomProduct.price_in_hand'
        db.delete_column(u'shop_customproduct', 'price_in_hand')


    models = {
        u'shop.cart': {
            'Meta': {'ordering': "('-creation_date',)", 'object_name': 'Cart'},
            'checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
            'price_in_hand': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
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
            'price_in_hand': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
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