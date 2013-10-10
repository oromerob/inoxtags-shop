# -*- coding:utf-8 -*-
from django.forms import ModelForm

from apps.billing.models import OrderItem, Invoice, Order


class StaffOrderCreateForm(ModelForm):

    class Meta:
        model = Order
        fields = ['user', 'hand_delivery']


class StaffOrderItemAddForm(ModelForm):

    class Meta:
        model = OrderItem
        exclude = ('order', 'price', 'price_special_1', 'price_special_2', 'price_special_3', 'price_special_4', 'price_in_hand', 'made', 'processing',)


class StaffInvoiceCreateForm(ModelForm):

    class Meta:
        model = Invoice
        exclude = ('order', 'rect',)


class StaffShippingCodeForm(ModelForm):

    class Meta:
        model = Order
        fields = ['shipping_code']
