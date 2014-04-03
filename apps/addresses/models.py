#-*- coding:utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Address(models.Model):

    COUNTRIES = settings.COUNTRIES

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(
        max_length=200,
        verbose_name=_('address name'),
    )
    address = models.CharField(
        max_length=255,
        verbose_name=_('address'),
    )
    postal_code = models.CharField(
        max_length=5,
        verbose_name=_('postal code'),
    )
    town = models.CharField(
        max_length=200,
        verbose_name=_('town'),
    )
    country = models.CharField(
        max_length=200,
        choices=COUNTRIES,
        default='ES',
        verbose_name=_('country'),
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
