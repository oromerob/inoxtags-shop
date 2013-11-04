from django.contrib import admin

from apps.content_pages.models import HomeSlider, HomeFeaturette, AboutPage


class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ['title','text','btn_link','btn_txt','is_active']


class HomeFeaturetteAdmin(admin.ModelAdmin):
    list_display = ['slogan','subslogan','is_active']


class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['title','content','active']


admin.site.register(HomeSlider, HomeSliderAdmin)
admin.site.register(HomeFeaturette, HomeFeaturetteAdmin)
admin.site.register(AboutPage, AboutPageAdmin)
