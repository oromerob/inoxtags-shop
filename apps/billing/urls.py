from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from apps.billing.views import (
    OrderListView,
    OrderDetailView,
    InvoiceListView,
    InvoicePdfView,
    InvoiceRectPdfView,
    UnpayedCheckoutView,
)


urlpatterns = patterns('',
    url(r'^accounts/orders/$', login_required(OrderListView.as_view()), name='user_order_list'),
    url(r'^accounts/order/(?P<pk>\d+)/$', login_required(OrderDetailView.as_view()), name='user_order_detail'),
    url(r'^accounts/invoices/$', login_required(InvoiceListView.as_view()), name='user_invoice_list'),
    url(r'^accounts/invoice/(?P<pk>\d+)/$', login_required(InvoicePdfView.as_view()), name='user_invoice_pdf'),
    url(r'^accounts/invoice_rect/(?P<pk>\d+)/$', login_required(InvoiceRectPdfView.as_view()), name='user_invoice_rect_pdf'),
    url(r'^checkout/done/$', login_required(UnpayedCheckoutView.as_view()), name='unpayed_checkout'),
)
