from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from apps.backend_braintree.views import CheckoutSummaryView, PaymentResultView


urlpatterns = patterns('',
    url(r'^checkout/$', login_required(CheckoutSummaryView.as_view()), name='checkout_summary'),
    url(r'^payment/result/$', login_required(PaymentResultView.as_view()), name='payment_result'),
)
