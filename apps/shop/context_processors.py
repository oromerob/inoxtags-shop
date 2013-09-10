#-*- coding:utf-8 -*-
"""
Context processor to have access to the session cart data in all the views.
"""
from apps.shop.models import Cart


def cart_context(request):
    try:
        cart_id = request.session['CART_ID']
        cart = Cart.objects.filter(checked_out=False).get(id=cart_id)
    except:
        cart = None

    if cart:

        count = cart.get_count()
        price = cart.get_price(request.user)

        cart_products = cart.customproduct_set.all()

    else:
        cart_products = None
        price = 0
        count = 0

    return {
        'Cart': cart,
        'CartPrice': price,
        'CartProducts': cart_products,
        'CountCartItems': count,
    }
