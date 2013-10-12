#-*- coding:utf-8 -*-
"""
Stripe payment views.
"""
from django.views.generic.base import View
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render

import stripe

from inoxtags.settings import STRIPE_SECRET, STRIPE_PUBLISHABLE

stripe.api_key = STRIPE_SECRET


class CheckoutSummaryView(View):

    template_name = 'stripe/checkout_summary.html'

    def post(self, request, *args, **kwargs):
        # Get the CartPrice
        context_price = RequestContext(request).get('CartPrice')
        price_cents = context_price * 100

        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']

        # Create the charge on Stripe's servers - this will charge the user's
        # card
        try:
            charge = stripe.Charge.create(
                amount=price_cents,  # amount in cents, again
                currency="eur",
                card=token,
                description="payinguser@example.com"
            )
        except stripe.CardError, e:
              # The card has been declined
            pass

        if charge:
            HttpResponseRedirect('/payment/success')
        else:
            HttpResponseRedirect('/payment/error')

        return render(request, self.template_name)

    def get_context_data(self, **kwargs):
        context = super(CheckoutSummaryView, self).get_context_data(**kwargs)
        context['stripe_key'] = STRIPE_PUBLISHABLE
        return context
