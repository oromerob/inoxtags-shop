from .models import (
    ProjectSettings,
    Tag,
    Country,
)
from django.contrib import admin


class ProjectSettingsAdmin(admin.ModelAdmin):
    list_display = ['name','company','owner','creation_date','is_active','registration_open']


class TagAdmin(admin.ModelAdmin):
    list_display = ['tag','is_active']



admin.site.register(ProjectSettings, ProjectSettingsAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Country)
