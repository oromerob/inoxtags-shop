from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from apps.backend_stripe.views import CheckoutSummaryView, ChargeView, ChargeSuccessView, ChargeErrorView


urlpatterns = patterns('',
    url(r'^checkout/$', login_required(CheckoutSummaryView.as_view()), name='checkout_summary_stripe'),
    url(r'^charge/$', login_required(ChargeView.as_view()), name='stripe_charge'),
    url(r'^charge/success/$', login_required(ChargeSuccessView.as_view()), name='stripe_charge_success'),
    url(r'^charge/error/$', login_required(ChargeErrorView.as_view()), name='stripe_charge_error'),
)
