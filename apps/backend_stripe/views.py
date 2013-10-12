#-*- coding:utf-8 -*-
"""
Stripe payment views.
"""
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render

import stripe

from inoxtags.settings import STRIPE_SECRET

stripe.api_key = STRIPE_SECRET


class CheckoutSummaryView(TemplateView):

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
