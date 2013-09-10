from apps.settings.models import *
from django.contrib import admin


class ProjectSettingsAdmin(admin.ModelAdmin):
    list_display = ['name','company','owner','creation_date','is_active','registration_open']


class TagAdmin(admin.ModelAdmin):
    list_display = ['tag','is_active']


class TosAdmin(admin.ModelAdmin):
    list_display = ['terms','privacity']


admin.site.register(ProjectSettings,ProjectSettingsAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Tos,TosAdmin)
