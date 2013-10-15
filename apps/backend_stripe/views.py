#-*- coding:utf-8 -*-
"""
Stripe payment views.
"""
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.template import RequestContext
from django.http import HttpResponseRedirect
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

import stripe

from inoxtags.settings import STRIPE_SECRET, STRIPE_PUBLISHABLE
from apps.backend_stripe.forms import StripeForm
from apps.billing.models import Iva, Order, OrderItem

stripe.api_key = STRIPE_SECRET


class CheckoutSummaryView(TemplateView):

    template_name = 'stripe/checkout_summary.html'

    def get_context_data(self, **kwargs):
        context = super(CheckoutSummaryView, self).get_context_data(**kwargs)
        context_price = RequestContext(self.request).get('CartPrice')
        context['price_cents'] = int(context_price * 100)
        context['stripe_key'] = STRIPE_PUBLISHABLE
        return context


class ChargeView(FormView):

    success_url = '/charge/success/'
    form_class = StripeForm

    def form_valid(self, form):
        # Get the CartPrice
        context_price = RequestContext(self.request).get('CartPrice')
        price_cents = int(context_price * 100)

        # Creates the description
        count_items = RequestContext(self.request).get('CountCartItems')
        cart = RequestContext(self.request).get('Cart')
        description = str(count_items) + ' items(' + str(context_price) + '€) from cart #' + str(cart)

        # Get the products in the current cart
        product_list = RequestContext(self.request).get('CartProducts')

        # Get the credit card details submitted by the form
        token = form.cleaned_data['stripeToken']

        # Create the charge on Stripe's servers - this will charge the user's
        # card
        try:
            charge = stripe.Charge.create(
                amount=price_cents,  # amount in cents, again
                currency="eur",
                card=token,
                description=description
            )

            # Once the charge is made, creates the order, the order items,
            # sends the confirmation email and marks the cart as checked out.
            iva = Iva.objects.filter(is_active=True).get()
            count_total = cart.get_count_total()
            user = self.request.user

            # Creates the order
            order = Order.objects.create(
                cart=cart,
                user=user,
                to=user.name,
                address=user.shipping_address,
                postal_code=user.shipping_code,
                town=user.shipping_town,
                country=user.shipping_country.country,
                count=count_total,
                price=context_price,
                iva=Decimal(str(iva)),
                payed=True
            )

            # Creates the order items
            for item in product_list:
                OrderItem.objects.create(
                    order=order,
                    quantity=item.quantity,
                    product=item.product,
                    color=item.color,
                    front_main=item.front_main,
                    front_tel=item.front_tel,
                    back_1=item.back_1,
                    back_2=item.back_2,
                    back_3=item.back_3,
                    price=item.price,
                    price_special_1=item.price_special_1,
                    price_special_2=item.price_special_2,
                    price_special_3=item.price_special_3,
                    price_special_4=item.price_special_4,
                    price_in_hand=item.price_in_hand,
                    made=item.made,
                    repetition=item.repetition
                )

            # Send a confirmation email
            subject = _("Comanda gestionada correctament a la web d'INOXtags.")
            email = user.email
            html_content = render_to_string('email/conf_order.html', {'order': order, 'products': product_list})
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(subject, text_content, to=[email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # Mark the cart as checked out
            cart.checked_out = True
            cart.save()

        except stripe.CardError:
              # The card has been declined
            pass

        if charge:

            # Once the charge is made, creates the order, the order items,
            # sends the confirmation email and marks the cart as checked out.
            iva = Iva.objects.filter(is_active=True).get()
            count_total = cart.get_count_total()
            user = self.request.user

            # Creates the order
            order = Order.objects.create(
                cart=cart,
                user=user,
                to=user.name,
                address=user.shipping_address,
                postal_code=user.shipping_code,
                town=user.shipping_town,
                country=user.shipping_country.country,
                count=count_total,
                price=context_price,
                iva=Decimal(str(iva)),
                payed=True
            )

            # Creates the order items
            for item in product_list:
                OrderItem.objects.create(
                    order=order,
                    quantity=item.quantity,
                    product=item.product,
                    color=item.color,
                    front_main=item.front_main,
                    front_tel=item.front_tel,
                    back_1=item.back_1,
                    back_2=item.back_2,
                    back_3=item.back_3,
                    price=item.price,
                    price_special_1=item.price_special_1,
                    price_special_2=item.price_special_2,
                    price_special_3=item.price_special_3,
                    price_special_4=item.price_special_4,
                    price_in_hand=item.price_in_hand,
                    made=item.made,
                    repetition=item.repetition
                )

            # Send a confirmation email
            subject = _("Comanda gestionada correctament a la web d'INOXtags.")
            email = user.email
            html_content = render_to_string('email/conf_order.html', {'order': order, 'products': product_list})
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(subject, text_content, to=[email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # Mark the cart as checked out
            cart.checked_out = True
            cart.save()
        else:
            HttpResponseRedirect('/charge/error/')

        return super(ChargeView, self).form_valid(form)


class ChargeSuccessView(TemplateView):

    template_name = 'stripe/payment_success.html'


class ChargeErrorView(TemplateView):

    template_name = 'stripe/payment_error.html'
