#-*- coding:utf-8 -*-
"""
Shop and cart views.
"""
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .models import Product, Category, CustomProduct, Cart, Shipping
from .forms import CustomProductForm


class ShopMainView(ListView):

    model = Product
    context_object_name = 'product_list'
    template_name = 'shop/shop_main.html'

    def get_context_data(self, **kwargs):
        context = super(ShopMainView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ShopCategoryView(ListView):

    context_object_name = 'product_list'
    template_name = 'shop/shop_category.html'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        objects = Product.objects.filter(category=category)
        return objects

    def get_context_data(self, **kwargs):
        context = super(ShopCategoryView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CustomProductCreateView(CreateView):

    template_name = 'shop/shop_product_form.html'
    form_class = CustomProductForm
    success_url = '/shop/cart/'
    model = CustomProduct

    def dispatch(self, *args, **kwargs):
        self.product = get_object_or_404(Product, slug=kwargs['slug'])
        return super(CustomProductCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        cart_id = self.request.session.get('CART_ID')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id, checked_out=False)
            except:
                cart = Cart.objects.create()
                self.request.session['CART_ID'] = cart.id
        else:
            cart = Cart.objects.create()
            self.request.session['CART_ID'] = cart.id
        self.object = form.save(commit=False)
        self.object.cart = cart
        self.object.product = self.product
        self.object.price_normal = self.product.category.price_normal
        self.object.price_prof = self.product.category.price_prof
        self.object.price_in_hand = self.product.category.price_in_hand
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CustomProductCreateView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['product'] = self.product
        return context


class CartView(ListView):

    model = Product
    context_object_name = 'product_list'
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['product_list'] = Product.objects.all()
        context['shipping'] = Shipping.objects.get()
        return context


class CustomProductDeleteView(DeleteView):

    model = CustomProduct
    success_url = '/shop/cart/'
    template_name = 'shop/custom_product_delete.html'
