from apps.shop.models import *
from django.contrib import admin


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category','price','price_special_1','price_special_2','price_special_3','price_special_4','has_color','has_front_main','has_front_tel','has_back_1','has_back_2','has_back_3']
    ordering = ['price']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','description']
    ordering = ['category']


class CartAdmin(admin.ModelAdmin):
    list_display = ['id','creation_date','checked_out']
    ordering = ['id']


class CustomProductAdmin(admin.ModelAdmin):
    list_display = ['id','cart','quantity','product','color','front_main','front_tel','back_1','back_2','back_3','repetition']
    ordering = ['id']



admin.site.register(Category,CategoryAdmin)
admin.site.register(Color)
admin.site.register(Product,ProductAdmin)
admin.site.register(Shape)
admin.site.register(Cart,CartAdmin)
admin.site.register(CustomProduct,CustomProductAdmin)
