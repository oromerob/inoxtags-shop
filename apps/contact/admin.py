from apps.contact.models import Contact
from django.contrib import admin


class ContactAdmin(admin.ModelAdmin):
    list_display = ['creation_date', 'name', 'email', 'message']
    ordering = ['creation_date']

admin.site.register(Contact, ContactAdmin)
