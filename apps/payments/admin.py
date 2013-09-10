from django.contrib import admin
from apps.payments.models import *


class BraintreeRawLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp','user','queryset']
    ordering = ['-id']

class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ['user','amount','transaction_id']
    ordering = ['-id']

class PaymentErrorLogAdmin(admin.ModelAdmin):
    list_display = ['user','amount','cart','error']
    ordering = ['-id']

admin.site.register(BraintreeRawLog,BraintreeRawLogAdmin)
admin.site.register(PaymentLog,PaymentLogAdmin)
admin.site.register(PaymentErrorLog,PaymentErrorLogAdmin)
