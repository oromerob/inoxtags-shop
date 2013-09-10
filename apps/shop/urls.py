from django.conf.urls import patterns, include, url

from apps.shop.views import ShopMainView, ShopCategoryView, CustomProductCreateView, CartView, CustomProductDeleteView


urlpatterns = patterns('',
    url(r'^$', ShopMainView.as_view(), name='shop_main'),
    url(r'^(?P<slug>[-\w]+)$', ShopCategoryView.as_view(), name='shop_category'),
    url(r'^product/(?P<slug>[-\w]+)$', CustomProductCreateView.as_view(), name='shop_product_create'),
    url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^cart/remove/(?P<pk>\d+)$', CustomProductDeleteView.as_view(), name='cart_remove'),
)
