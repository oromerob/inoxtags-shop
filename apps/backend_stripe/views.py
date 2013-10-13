#-*- coding:utf-8 -*-
"""
Stripe payment views.
"""
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render

import stripe

from inoxtags.settings import STRIPE_SECRET, STRIPE_PUBLISHABLE
from apps.backend_stripe.forms import StripeForm

stripe.api_key = STRIPE_SECRET


class CheckoutSummaryView(TemplateView):

    template_name = 'stripe/checkout_summary.html'

    def get_context_data(self, **kwargs):
        context = super(CheckoutSummaryView, self).get_context_data(**kwargs)
        context_price = RequestContext(self.request).get('CartPrice')
        context['price_cents'] = context_price * 100
        context['stripe_key'] = STRIPE_PUBLISHABLE
        return context


class ChargeView(FormView):

    success_url = '/payment/success/'
    form_class = StripeForm

    def form_valid(self, form):
        # Get the CartPrice
        context_price = RequestContext(self.request).get('CartPrice')
        price_cents = context_price * 100

        # Get the credit card details submitted by the form
        token = self.request.POST['stripeToken']

        # Create the charge on Stripe's servers - this will charge the user's
        # card
        try:
            stripe.Charge.create(
                amount=price_cents,  # amount in cents, again
                currency="eur",
                card=token,
                description="payinguser@example.com"
            )
        except stripe.CardError:
              # The card has been declined
            pass

        return super(ChargeView, self).form_valid(form)
