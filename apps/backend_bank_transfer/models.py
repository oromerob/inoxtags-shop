#-*- coding:utf-8 -*-
from django.db import models
from django.conf import settings

from apps.shop.models import Cart


class PreOrder(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    cart = models.ForeignKey(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=2)
    payed = models.BooleanField(default=False, verbose_name="Pagat")
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s / %s' % (self.creation_date.year, self.id)

    class Meta:
        ordering = ('-creation_date',)
