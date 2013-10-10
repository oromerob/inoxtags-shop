from apps.backend_bank_transfer.models import *
from django.contrib import admin


class PreOrderAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'user', 'cart', 'price', 'payed', 'deleted']
    ordering = ['-id']


admin.site.register(PreOrder, PreOrderAdmin)
