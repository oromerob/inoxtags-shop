#-*- coding:utf-8 -*-

from django.db import models
from django.conf import settings

from apps.shop.models import Cart


class BraintreeRawLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    queryset = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % (self.id)


class PaymentLog(models.Model):
    """
    Captures raw charges made to a users credit card. Extra info related to
    this payment should be a OneToOneField referencing this model.
    """

    rawlog = models.ForeignKey(BraintreeRawLog)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    timestamp = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=128)

    def __unicode__(self):
        return u'%s charged %s - %s' % (self.user, self.amount, self.transaction_id)


class PaymentErrorLog(models.Model):
    rawlog = models.ForeignKey(BraintreeRawLog)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    timestamp = models.DateTimeField(auto_now=True)
    cart = models.ForeignKey(Cart)
    error = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s ha intentat pagar %s de %s. Error: %s' % (self.user, self.cart, self.amount, self.error)
