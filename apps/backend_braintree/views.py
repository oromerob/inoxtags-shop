#-*- coding:utf-8 -*-
"""
Checkout views.
"""
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.contrib.sites.models import Site
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

import braintree

from apps.backend_braintree.models import BraintreeRawLog, PaymentLog, PaymentErrorLog
from apps.billing.models import Iva, Order, OrderItem


class CheckoutSummaryView(TemplateView):

    template_name = 'braintree/checkout_summary.html'

    def get_context_data(self, **kwargs):
        context = super(CheckoutSummaryView, self).get_context_data(**kwargs)
        context_price = RequestContext(self.request).get('CartPrice')
        domain = Site.objects.get_current().domain
        redirect_url = 'http://' + domain + '/payment/result/'
        context['action'] = braintree.TransparentRedirect.url()
        context['tr_data'] = braintree.Transaction.tr_data_for_sale({
            "transaction": {
                "type": "sale",
                "amount": context_price,
            }
        }, redirect_url)
        return context


class PaymentResultView(TemplateView):

    template_name = 'braintree/payment_result.html'

    def get(self, request, *args, **kwargs):
        cart = RequestContext(request).get('Cart')
        price = RequestContext(request).get('CartPrice')
        product_list = RequestContext(request).get('CartProducts')
        query_string = 'http_status=' + request.GET.get('http_status') + '&id=' + request.GET.get('id', '') + '&kind=' + request.GET.get('kind') + '&hash=' + request.GET.get('hash')
        raw_log = BraintreeRawLog.objects.create(user=request.user, queryset=query_string)
        result = braintree.TransparentRedirect.confirm(query_string)
        if result.is_success:
            self.status = None
            PaymentLog.objects.create(rawlog=raw_log, user=request.user, amount=price, transaction_id=result.transaction.id)
            iva = Iva.objects.filter(is_active=True).get()
            count_total = cart.get_count_total()

            # Creates the order

            order = Order.objects.create(
                cart=cart,
                user=request.user,
                to=request.user.name,
                address=request.user.shipping_address,
                postal_code=request.user.shipping_code,
                town=request.user.shipping_town,
                country=request.user.shipping_country.country,
                count=count_total,
                price=price,
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
            email = request.user.email
            html_content = render_to_string('email/conf_order.html', {'order': order, 'products': product_list})
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(subject, text_content, to=[email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # Mark the cart as checked out

            cart.checked_out = True
            cart.save()

        else:
            self.status = result.message
            PaymentErrorLog.objects.create(rawlog=raw_log, user=request.user, amount=price, cart=cart, error=self.status)

        return super(PaymentResultView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PaymentResultView, self).get_context_data(**kwargs)
        context['status'] = self.status
        return context
