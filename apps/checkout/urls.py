from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from apps.checkout.views import CheckoutSummaryView, PaymentResultView, BankTransferView, OrderListView, OrderDetailView, InvoiceListView, InvoicePdfView, InvoiceRectPdfView


urlpatterns = patterns('',
    url(r'^checkout/$', login_required(CheckoutSummaryView.as_view()), name='checkout_summary'),
    url(r'^payment/result/$', login_required(PaymentResultView.as_view()), name='payment_result'),
    url(r'^payment/bank_transfer/$', login_required(BankTransferView.as_view()), name='bank_transfer'),
    url(r'^accounts/orders/$', login_required(OrderListView.as_view()), name='user_order_list'),
    url(r'^accounts/order/(?P<pk>\d+)/$', login_required(OrderDetailView.as_view()), name='user_order_detail'),
    url(r'^accounts/invoices/$', login_required(InvoiceListView.as_view()), name='user_invoice_list'),
    url(r'^accounts/invoice/(?P<pk>\d+)/$', login_required(InvoicePdfView.as_view()), name='user_invoice_pdf'),
    url(r'^accounts/invoice_rect/(?P<pk>\d+)/$', login_required(InvoiceRectPdfView.as_view()), name='user_invoice_rect_pdf'),
)
