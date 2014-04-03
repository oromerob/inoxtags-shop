#-*- coding:utf-8 -*-
from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from .models import Shipping


class ShippingAdmin(admin.ModelAdmin):
    '''formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }'''
    filter_horizontal = ('countries',)


admin.site.register(Shipping, ShippingAdmin)
