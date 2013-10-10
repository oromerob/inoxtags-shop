#-*- coding:utf-8 -*-
"""
Checkout views.
"""
from django.views.generic import ListView, DetailView

from apps.pdf.views import RenderPDF

from apps.billing.models import Order, Invoice, RectInvoice
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
