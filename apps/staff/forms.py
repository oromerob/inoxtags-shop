# -*- coding:utf-8 -*-
from django.forms import ModelForm

from apps.billing.models import OrderItem, Invoice, Order


class StaffOrderCreateForm(ModelForm):

    class Meta:
        model = Order
        fields = ['user']


class StaffOrderItemAddForm(ModelForm):

    class Meta:
        model = OrderItem
        fields = (
            'quantity',
            'product',
            'color',
            'front_main',
            'front_tel',
            'back_1',
            'back_2',
            'back_3',
            'repetition'
        )


class StaffInvoiceCreateForm(ModelForm):

    class Meta:
        model = Invoice
        exclude = ('order', 'rect',)


class StaffShippingCodeForm(ModelForm):

    class Meta:
        model = Order
        fields = ['shipping_code']
