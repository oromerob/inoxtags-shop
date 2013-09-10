from django.contrib import admin

from apps.content_pages.models import HomeSlider, HomeFeaturette


class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ['title','text','btn_link','btn_txt','is_active']


class HomeFeaturetteAdmin(admin.ModelAdmin):
    list_display = ['slogan','subslogan','is_active']


admin.site.register(HomeSlider, HomeSliderAdmin)
admin.site.register(HomeFeaturette, HomeFeaturetteAdmin)
