from django.contrib import admin

from ckeditor.widgets import CKEditorWidget

from .models import (
    HomeSlider,
    HomeFeaturette,
    StaticPage,
)


class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ['title','text','btn_link','btn_txt','is_active']


class HomeFeaturetteAdmin(admin.ModelAdmin):
    list_display = ['slogan','subslogan','is_active']



class StaticPageAdmin(admin.ModelAdmin):
    list_display = ['name', 'title']


admin.site.register(HomeSlider, HomeSliderAdmin)
admin.site.register(HomeFeaturette, HomeFeaturetteAdmin)
admin.site.register(StaticPage, StaticPageAdmin)
