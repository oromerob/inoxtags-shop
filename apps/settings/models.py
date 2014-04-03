#-*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
from django.conf import settings

from transmeta import TransMeta


class ProjectSettings(models.Model):

    COUNTRIES = settings.COUNTRIES

    name = models.CharField(max_length=100)     # Brand
    company = models.CharField(max_length=100)  # Legal name
    owner = models.CharField(max_length=100)    # Owner
    description = models.TextField(blank=True)
    creation_date = models.DateField()
    is_active = models.BooleanField(default=True)
    logo_font = models.FileField(upload_to='project')
    logo = models.ImageField(upload_to='project', blank=True)
    # Registration settings
    registration_open = models.BooleanField(default=True, verbose_name="REGISTRATION_OPEN")
    # Contact data
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    cp = models.CharField(max_length=8)
    town = models.CharField(max_length=100)
    country = models.CharField(max_length=100, choices=COUNTRIES)
    # Invoice data
    tax_code = models.CharField(max_length=100)
    invoice_address = models.CharField(max_length=200)
    invoice_cp = models.CharField(max_length=8)
    invoice_town = models.CharField(max_length=100)
    invoice_country = models.CharField(max_length=100, choices=COUNTRIES)
    # Bank transfer data
    bank_account = models.CharField(max_length=100)
    bank_iban = models.CharField(max_length=100)


    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Project settings"
        verbose_name = "Project settings"


class Tag(models.Model):
    __metaclass__ = TransMeta

    tag = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.tag

    class Meta:
        translate = ('tag',)


class Country(models.Model):
    __metaclass__ = TransMeta

    COUNTRIES = settings.COUNTRIES

    code = models.CharField(max_length=25, choices=COUNTRIES)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
        translate = ('name',)
        verbose_name_plural = 'countries'
