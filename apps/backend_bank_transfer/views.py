#-*- coding:utf-8 -*-
"""
Checkout views.
"""
from django.views.generic.base import TemplateView
from django.template import RequestContext
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


from apps.billing.models import Iva
from apps.backend_bank_transfer.models import PreOrder
from apps.settings.models import ProjectSettings


class BankTransferView(TemplateView):

    template_name = 'bank_transfer/bank_transfer.html'

    def get(self, request, *args, **kwargs):
        cart = RequestContext(request).get('Cart')
        price = RequestContext(request).get('CartPrice')
        product_list = RequestContext(request).get('CartProducts')
        iva = Iva.objects.filter(is_active=True).get()
        transfer_data = ProjectSettings.objects.values('company', 'invoice_address', 'invoice_cp', 'invoice_town', 'invoice_country', 'bank_account', 'bank_iban').get()

        # Creates a PreOrder

        pre_order = PreOrder.objects.create(cart=cart, user=request.user, price=price, iva=Decimal(str(iva)), payed=False, deleted=False)

        # Mark the cart as checked out

        cart.checked_out = True
        cart.save()

        # Send a confirmation email with the transfer data

        subject = _("Dades d'INOXtags per tramitar comanda.")
        email = request.user.email
        html_content = render_to_string('email/bank_transfer.html', {'pre_order':pre_order, 'products':product_list, 'transfer_data':transfer_data})
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, to=[email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return super(BankTransferView, self).get(request, *args, **kwargs)
