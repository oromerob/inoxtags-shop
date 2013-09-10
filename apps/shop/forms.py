#-*- coding:utf-8 -*-
"""
Custom forms and validation code for custom user registration
"""

from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.shop.models import CustomProduct



class CustomProductForm(forms.ModelForm):

    class Meta:
        model = CustomProduct
        fields = ('quantity', 'color', 'front_main', 'front_tel', 'back_1', 'back_2', 'back_3', 'repetition')
