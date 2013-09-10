from apps.checkout.models import *
from django.contrib import admin


class IvaAdmin(admin.ModelAdmin):
    list_display = ['iva', 'is_active']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'user', 'creation_date', 'price', 'count', 'payed', 'hand_delivery', 'made', 'shipped', 'deleted']
    ordering = ['-id']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['made', 'quantity', 'product', 'color', 'front_main', 'front_tel', 'back_1', 'back_2', 'back_3', 'repetition']
    ordering = ['-id']


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'user', 'order', 'concept', 'price', 'rect']
    ordering = ['-id']


class RectInvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'invoice', 'price']
    ordering = ['-id']


class PreOrderAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'user', 'cart', 'price', 'payed', 'deleted']
    ordering = ['-id']


admin.site.register(Iva, IvaAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(RectInvoice, RectInvoiceAdmin)
admin.site.register(PreOrder, PreOrderAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
