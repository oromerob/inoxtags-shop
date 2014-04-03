#-*- coding:utf-8 -*-
from django.db import models
from decimal import Decimal
from django.utils.translation import ugettext as _

from transmeta import TransMeta

from apps.settings.models import Country
from apps.billing.models import Iva


class Shipping(models.Model):
    __metaclass__ = TransMeta

    name = models.CharField(max_length=100, verbose_name='Name')
    description = models.TextField(verbose_name='Description')
    delivery_time = models.CharField(max_length=200, verbose_name='Delivery time')
    slogan = models.CharField(max_length=200, verbose_name='Slogan')
    amount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Amount')
    countries = models.ManyToManyField(Country)

    def __unicode__(self):
        return self.name

    def amount_base(self):
        iva = Iva.objects.get()
        return self.amount / (1 + (Decimal(str(iva)) / 100))

    class Meta:
        translate = ('name', 'description', 'slogan', )
