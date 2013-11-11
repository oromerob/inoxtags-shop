#-*- coding:utf-8 -*-
"""
Checkout views.
"""
from django import http
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.template import RequestContext
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from apps.pdf.views import RenderPDF

from .models import Order, Invoice, RectInvoice, Iva, OrderItem
from apps.settings.models import ProjectSettings


class OrderListView(ListView):

    template_name = 'checkout/order_list.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        return Order.objects.filter(deleted=False).filter(user=self.request.user).order_by('-creation_date')


class OrderDetailView(DetailView):

    template_name = 'checkout/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['product_list'] = self.object.orderitem_set.all()
        return context


class InvoiceListView(ListView):

    template_name = 'checkout/invoice_list.html'
    context_object_name = 'invoice_list'

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(InvoiceListView, self).get_context_data(**kwargs)
        context['rect_invoice_list'] = RectInvoice.objects.filter(user=self.request.user)
        context['order_list'] = Order.objects.filter(user=self.request.user).filter(deleted=False).filter(invoice=None)
        return context


class InvoicePdfView(RenderPDF, DetailView):

    template_name = 'pdf/invoice_pdf.html'
    context_object_name = 'invoice'

    def get_object(self, queryset=None):
        object = Invoice.objects.filter(user=self.request.user).get(pk=self.kwargs.get('pk'))
        object.tags = object.order.tags()
        object.data = ProjectSettings.objects.values('name', 'company', 'tax_code', 'invoice_address', 'invoice_cp', 'invoice_town', 'invoice_country', 'logo_font', 'phone', 'email').get()
        return object


class InvoiceRectPdfView(RenderPDF, DetailView):

    template_name = 'pdf/invoice_rect_pdf.html'
    context_object_name = 'invoice'

    def get_object(self, queryset=None):
        object = RectInvoice.objects.filter(user=self.request.user).get(pk=self.kwargs.get('pk'))
        object.data = ProjectSettings.objects.values('name', 'company', 'tax_code', 'invoice_address', 'invoice_cp', 'invoice_town', 'invoice_country', 'logo_font', 'phone', 'email').get()
        return object


class UnpayedCheckoutView(TemplateView):

    template_name = 'checkout/unpayed_checkout.html'

    '''def dispatch(self, request, *args, **kwargs):
        if not request.user.hand_delivery or not request.user.modey_order:
            raise http.Http404
        return super(UnpayedCheckoutView, self).dispatch(request, *args, **kwargs)'''

    def get(self, request, *args, **kwargs):
        cart = RequestContext(request).get('Cart')
        price = RequestContext(request).get('CartPrice')
        product_list = RequestContext(request).get('CartProducts')
        iva = Iva.objects.filter(is_active=True).get()
        user = request.user
        count_total = cart.get_count_total()

        # Creates the Order
        order = Order.objects.create(
            cart=cart,
            user=user,
            to=user.name,
            address=user.shipping_address,
            postal_code=user.shipping_code,
            town=user.shipping_town,
            country=user.shipping_country.country,
            count=count_total,
            price=price,
            iva=Decimal(str(iva)),
            payed=False,
            hand_delivery=user.hand_delivery,
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
        # Mark the cart as checked out

        cart.checked_out = True
        cart.save()

        # Send a confirmation email
        subject = _("Comanda gestionada correctament a la web d'INOXtags.")
        email = user.email
        html_content = render_to_string('email/conf_order.html', {'order': order, 'products': product_list})
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, to=[email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return super(UnpayedCheckoutView, self).get(request, *args, **kwargs)
