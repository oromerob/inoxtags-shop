# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BraintreeRawLog'
        db.create_table(u'payments_braintreerawlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.InoxUser'])),
            ('queryset', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'payments', ['BraintreeRawLog'])

        # Adding model 'PaymentLog'
        db.create_table(u'payments_paymentlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rawlog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['payments.BraintreeRawLog'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.InoxUser'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'payments', ['PaymentLog'])

        # Adding model 'PaymentErrorLog'
        db.create_table(u'payments_paymenterrorlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rawlog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['payments.BraintreeRawLog'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.InoxUser'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Cart'])),
            ('error', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'payments', ['PaymentErrorLog'])


    def backwards(self, orm):
        # Deleting model 'BraintreeRawLog'
        db.delete_table(u'payments_braintreerawlog')

        # Deleting model 'PaymentLog'
        db.delete_table(u'payments_paymentlog')

        # Deleting model 'PaymentErrorLog'
        db.delete_table(u'payments_paymenterrorlog')


    models = {
        u'accounts.country': {
            'Meta': {'object_name': 'Country'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'accounts.inoxuser': {
            'Meta': {'object_name': 'InoxUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'invoice_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'invoice_extra_charge': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'invoice_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'invoice_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'invoice_tax_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'invoice_town': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_professional': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone_1': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'phone_2': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'share': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shipping_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'shipping_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'shipping_country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Country']", 'null': 'True', 'blank': 'True'}),
            'shipping_town': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'town': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.PartnerTown']", 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.PartnerZone']", 'null': 'True', 'blank': 'True'})
        },
        u'accounts.partnertown': {
            'Meta': {'object_name': 'PartnerTown'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'town'"}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.PartnerZone']"})
        },
        u'accounts.partnerzone': {
            'Meta': {'object_name': 'PartnerZone'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'zone'"}),
            'zone': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'payments.braintreerawlog': {
            'Meta': {'object_name': 'BraintreeRawLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'queryset': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.InoxUser']"})
        },
        u'payments.paymenterrorlog': {
            'Meta': {'object_name': 'PaymentErrorLog'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Cart']"}),
            'error': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rawlog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payments.BraintreeRawLog']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.InoxUser']"})
        },
        u'payments.paymentlog': {
            'Meta': {'object_name': 'PaymentLog'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rawlog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payments.BraintreeRawLog']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.InoxUser']"})
        },
        u'shop.cart': {
            'Meta': {'ordering': "('-creation_date',)", 'object_name': 'Cart'},
            'checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['payments']