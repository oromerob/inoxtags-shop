from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from apps.backend_stripe.views import CheckoutSummaryView, ChargeView


urlpatterns = patterns('',
    url(r'^checkout/$', login_required(CheckoutSummaryView.as_view()), name='checkout_summary_stripe'),
    url(r'^charge/$', login_required(ChargeView.as_view()), name='stripe_charge'),
)
