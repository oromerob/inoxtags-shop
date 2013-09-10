#-*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField

from transmeta import TransMeta


class ProjectSettings(models.Model):
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
    country = models.CharField(max_length=100)
    # Invoice data
    tax_code = models.CharField(max_length=100)
    invoice_address = models.CharField(max_length=200)
    invoice_cp = models.CharField(max_length=8)
    invoice_town = models.CharField(max_length=100)
    invoice_country = models.CharField(max_length=100)
    # Bank transfer data
    bank_account = models.CharField(max_length=100)
    bank_iban = models.CharField(max_length=100)


    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Project settings"
        verbose_name = "Project settings"


class Tag(models.Model):
    tag = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.tag


class Tos(models.Model):
    __metaclass__ = TransMeta

    terms = RichTextField(verbose_name=_('terms of service'))
    privacity = RichTextField(verbose_name=_('privacity'))

    def __unicode__(self):
        return self.terms[:50]

    class Meta:
        verbose_name_plural = "Terms of service"
        translate = ('terms', 'privacity',)
