#-*- coding:utf-8 -*-
from decimal import Decimal
import datetime

from django.views.generic.edit import FormView, UpdateView, CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView, TemplateView
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse_lazy, reverse

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from apps.pdf.views import RenderPDF

from .forms import StaffOrderCreateForm, StaffOrderItemAddForm, StaffShippingCodeForm, StaffInvoiceCreateForm
from apps.billing.models import OrderItem, Invoice, Order, RectInvoice
from apps.backend_bank_transfer.models import PreOrder
from apps.shop.models import Iva
from apps.settings.models import ProjectSettings
from accounts.models import InoxUser


class StaffCheckoutView(FormView):

    template_name = 'staff/checkout.html'
    form_class = StaffOrderCreateForm
    success_url = '/shop/'

    def form_valid(self, form):
        cart = RequestContext(self.request).get('Cart')
        product_list = RequestContext(self.request).get('CartProducts')

        iva = Iva.objects.filter(is_active=True).get()

        # Creates the order from the form data

        order = form.save(commit=False)
        order.cart = cart
        order.to = order.user.name
        order.address = order.user.shipping_address
        order.postal_code = order.user.shipping_code
        order.town = order.user.shipping_town
        order.country = order.user.shipping_country.country
        order.count = cart.get_count_total()
        order.price = cart.get_price(order.user)
        order.iva = Decimal(str(iva))
        order.payed = False
        order.hand_delivery = order.user.hand_delivery
        if order.user.is_professional:
            if not order.user.hand_delivery:
                order.management = True
        order.save()

        # Creates the order items from the customized products

        for product in product_list:
            if order.user.is_professional:
                if order.user.hand_delivery:
                    price = product.price_in_hand
                else:
                    price = product.price_prof
            else:
                price = product.price_normal
            OrderItem.objects.create(
                order=order,
                quantity=product.quantity,
                product=product.product,
                color=product.color,
                front_main=product.front_main,
                front_tel=product.front_tel,
                back_1=product.back_1,
                back_2=product.back_2,
                back_3=product.back_3,
                price=price,
                made=product.made,
                repetition=product.repetition
            )

        # Mark the cart as checked out

        cart.checked_out = True
        cart.save()

        # Send the confirmation email

        mail = order.user.email
        try:
            if order.user.lang == "ca":
                subject = _("Nova comanda a INOXtags.com")
                html_content = render_to_string('email/conf_order_ca.html', {'order': order, 'product_list': product_list})
            elif order.user.lang == "es":
                subject = _("Nuevo pedido en INOXtags.com")
                html_content = render_to_string('email/conf_order_es.html', {'order': order, 'product_list': product_list})
            else:
                subject = _("Your new order from INOXtags.com")
                html_content = render_to_string('email/conf_order_en.html', {'order': order, 'product_list': product_list})
        except:
            subject = _("Your new order from INOXtags.com")
            html_content = render_to_string('email/conf_order_en.html', {'order': order, 'product_list': product_list})
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, to=[mail])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponseRedirect(self.get_success_url())


class StaffWorkshopView(ListView):

    template_name = 'staff/workshop.html'
    context_object_name = 'tag_list'
    queryset = OrderItem.objects.filter(made=False).order_by('product')

    def get_context_data(self, **kwargs):
        context = super(StaffWorkshopView, self).get_context_data(**kwargs)
        context['tag_count'] = OrderItem.objects.filter(made=False).order_by('id').count()
        return context


class StaffWorkshopPdfView(RenderPDF, ListView):

    template_name = 'pdf/workshop_pdf.html'
    context_object_name = 'item_list'
    queryset = OrderItem.objects.filter(made=False).order_by('product')


class StaffWorkshopMadeView(RedirectView):

    url = reverse_lazy('staff_workshop')

    def dispatch(self, *args, **kwargs):
        item = get_object_or_404(OrderItem, pk=self.kwargs.get('pk'))
        item.made = True
        item.save()
        return super(StaffWorkshopMadeView, self).dispatch(*args, **kwargs)


class StaffBankTransferListView(ListView):

    template_name = 'staff/bank_transfer_list.html'
    context_object_name = 'preorder_list'
    queryset = PreOrder.objects.filter(deleted=False).filter(payed=False).order_by('-id')


class StaffBankTransferDoneView(RedirectView):

    url = reverse_lazy('staff_bank_transfer_list')

    def dispatch(self, *args, **kwargs):
        pre_order = get_object_or_404(PreOrder, pk=self.kwargs.get('pk'))
        product_list = pre_order.cart.customproduct_set.all()
        count_total = pre_order.cart.get_count_total()

        # Creates the order

        user = pre_order.user
        if user.is_professional:
            if not user.hand_delivery:
                management = True

        order = Order.objects.create(
            cart=pre_order.cart,
            user=user,
            to=user.name,
            address=user.shipping_address,
            postal_code=user.shipping_code,
            town=user.shipping_town,
            country=user.shipping_country.country,
            count=count_total,
            price=pre_order.price,
            iva=Decimal(str(pre_order.iva)),
            payed=True,
            management=management,
        )

        # Creates the order items from the customized products

        for product in product_list:
            if order.user.is_professional:
                if order.user.hand_delivery:
                    price = product.price_in_hand
                else:
                    price = product.price_prof
            else:
                price = product.price_normal
            OrderItem.objects.create(
                order=order,
                quantity=product.quantity,
                product=product.product,
                color=product.color,
                front_main=product.front_main,
                front_tel=product.front_tel,
                back_1=product.back_1,
                back_2=product.back_2,
                back_3=product.back_3,
                price=price,
                made=product.made,
                repetition=product.repetition
            )

        # Auto generates the invoice if required

        if order.user.invoice_required:
            Invoice.objects.create(
                user=order.user,
                order=order,
                price=order.price,
                iva=order.iva
            )
            order.has_invoice = True
            order.save()

        # Mark the cart as checked out

        pre_order.payed = True
        pre_order.save()

        # Send the confirmation email

        mail = order.user.email
        try:
            if order.user.lang == "ca":
                subject = "Transferència rebuda a INOXtags.com"
                html_content = render_to_string('email/banktransfer_done_ca.html', {'order':order, 'product_list':product_list})
            elif order.user.lang == "es":
                subject = "Transferencia recibida en INOXtags.com"
                html_content = render_to_string('email/banktransfer_done_es.html', {'order':order, 'product_list':product_list})
            else:
                subject = "Wire transfer received successfully in INOXtags.com"
                html_content = render_to_string('email/banktransfer_done_en.html', {'order':order, 'product_list':product_list})
        except:
            subject = "Wire transfer received successfully in INOXtags.com"
            html_content = render_to_string('email/banktransfer_done_en.html', {'order':order, 'product_list':product_list})
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, to=[mail])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return super(StaffBankTransferDoneView, self).dispatch(*args, **kwargs)


class StaffHandDeliveryMixin(ListView):

    context_object_name = 'order_list'
    queryset = Order.objects.filter(deleted=False).filter(made=True).filter(shipped=False).filter(hand_delivery=True).order_by('user',)


class StaffHandDeliveryListView(StaffHandDeliveryMixin):

    template_name = 'staff/hand_delivery_list.html'


class StaffHandDeliveryPdfView(RenderPDF, StaffHandDeliveryMixin):

    template_name = 'pdf/hand_delivery_pdf.html'


class StaffHandDeliveryDoneView(RedirectView):

    url = reverse_lazy('staff_hand_delivery_list')

    def dispatch(self, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        order.shipped = True
        order.save()
        return super(StaffHandDeliveryDoneView, self).dispatch(*args, **kwargs)


class StaffHandDeliveryPayedView(RedirectView):

    url = reverse_lazy('staff_hand_delivery_list')

    def dispatch(self, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        order.mark_as_payed()
        return super(StaffHandDeliveryPayedView, self).dispatch(*args, **kwargs)


class StaffOrderList(ListView):

    template_name = 'staff/order_list.html'
    context_object_name = 'order_list'
    model = Order
    '''test_user = get_object_or_404(InoxUser, email='13.oriol@gmail.com')
    queryset = Order.objects.exclude(user=test_user)'''

    def dispatch(self, *args, **kwargs):
        for order in Order.objects.filter(made=False):
            order.check_made()
        return super(StaffOrderList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StaffOrderList, self).get_context_data(**kwargs)
        context['to_do'] = Order.objects.filter(deleted=False).filter(made=False).count()
        context['unpayed'] = Order.objects.filter(deleted=False).filter(made=True).filter(payed=False).count()
        context['undelivered'] = Order.objects.filter(deleted=False).filter(made=True).filter(hand_delivery=True).filter(shipped=False).count()
        context['unshipped'] = Order.objects.filter(deleted=False).filter(made=True).filter(hand_delivery=False).filter(shipped=False).count()
        return context


class StaffOrderDeleteListView(ListView):

    template_name = 'staff/order_delete_list.html'
    context_object_name = 'order_list'
    queryset = Order.objects.filter(deleted=False)


class StaffOrderDeleteView(RedirectView):

    url = reverse_lazy('staff_order_delete_list')

    def dispatch(self, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))

        # Mark the order as deleted

        order.mark_as_deleted()

        return super(StaffOrderDeleteView, self).dispatch(*args, **kwargs)


class StaffOrderModifyListView(ListView):

    template_name = 'staff/order_modify_list.html'
    context_object_name = 'order_list'
    queryset = Order.objects.filter(deleted=False).filter(shipped=False)


class StaffOrderAddItemView(FormView):

    template_name = 'staff/order_add_item.html'
    form_class = StaffOrderItemAddForm
    success_url = reverse_lazy('staff_order_modify_list')

    def form_valid(self, form):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        item = form.save(commit=False)
        item.order = order
        if order.user.is_professional:
            if order.user.hand_delivery:
                item.price = form.product.category.price_in_hand
            else:
                item.price = form.product.category.price_prof
        else:
            item.price = form.product.category.price_normal
        item.save()
        order.modify()
        return HttpResponseRedirect(self.get_success_url())


class StaffOrderDetailView(DetailView):

    template_name = 'staff/order_detail.html'
    context_object_name = 'order'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(StaffOrderDetailView, self).get_context_data(**kwargs)
        context['order_items'] = OrderItem.objects.filter(order=self.object)
        return context


class StaffOrderDeleteItemView(RedirectView):

    url = reverse_lazy('staff_order_modify_list')

    def dispatch(self, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, pk=self.kwargs.get('pk'))
        order = order_item.order
        order_item.delete()
        order.modify()
        product_list = order.orderitem_set.all()

        if not product_list:
            order.mark_as_deleted()

        return super(StaffOrderDeleteItemView, self).dispatch(*args, **kwargs)


class StaffOrderUnpayedListView(ListView):

    template_name = 'staff/order_unpayed_list.html'
    context_object_name = 'order_list'
    queryset = Order.objects.filter(deleted=False).filter(made=True).filter(payed=False)


class StaffOrderPayedView(RedirectView):

    url = reverse_lazy('staff_order_unpayed_list')

    def dispatch(self, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        order.mark_as_payed()
        return super(StaffOrderPayedView, self).dispatch(*args, **kwargs)


class StaffShipmentListView(TemplateView):

    template_name = 'staff/shipment_list.html'

    def get_context_data(self, **kwargs):
        context = super(StaffShipmentListView, self).get_context_data(**kwargs)
        context['es_order_list'] = Order.objects.filter(deleted=False).filter(made=True).filter(hand_delivery=False).filter(shipped=False).filter(country="Espanya")
        context['eu_order_list'] = Order.objects.filter(deleted=False).filter(made=True).filter(hand_delivery=False).filter(shipped=False).exclude(country="Espanya")
        return context


class StaffShipmentCodeAddListView(ListView):

    template_name = 'staff/shipment_code_add_list.html'
    context_object_name = 'order_list'
    queryset = Order.objects.filter(deleted=False).filter(made=True).filter(hand_delivery=False).order_by('country')

    def get_context_data(self, **kwargs):
        context = super(StaffShipmentCodeAddListView, self).get_context_data(**kwargs)
        context['form'] = StaffShippingCodeForm()
        return context


class StaffShipmentCodeAddFormView(UpdateView):

    form_class = StaffShippingCodeForm
    model = Order

    def get_success_url(self):
        return reverse('staff_shipment_shipped', kwargs={'pk':self.kwargs.get('pk'),})


class StaffShipmentShippedView(RedirectView):

    url = reverse_lazy('staff_shipment_code_add_list')

    def dispatch(self, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        order.shipped = True
        order.ship_date = datetime.datetime.now()
        order.save()
        return super(StaffShipmentShippedView, self).dispatch(*args, **kwargs)


class StaffOrderMarkHandDeliveryView(RedirectView):

    url = reverse_lazy('staff_shipment_list')

    def dispatch(self, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        order.hand_delivery = True
        order.save()
        return super(StaffOrderMarkHandDeliveryView, self).dispatch(*args, **kwargs)


class StaffShipmentCodeListView(ListView):

    template_name = 'staff/shipment_code_list.html'
    context_object_name = 'order_list'
    queryset = Order.objects.filter(deleted=False).filter(made=True).filter(hand_delivery=False).filter(shipped=True)


class StaffShipmentListPdfView(RenderPDF, TemplateView):

    template_name = 'pdf/shipment_list_pdf.html'

    def get_context_data(self, **kwargs):
        context = super(StaffShipmentListPdfView, self).get_context_data(**kwargs)
        context['es_1'] = Order.objects.filter(deleted=False).filter(made=True).filter(hand_delivery=False).filter(shipped=False).filter(country="Espanya").filter(count=1)
        context['es_2'] = Order.objects.filter(deleted=False).filter(made=True).filter(hand_delivery=False).filter(shipped=False).filter(country="Espanya").filter(count__in=[2, 3])
        context['es_3'] = Order.objects.filter(deleted=False).filter(made=True).filter(hand_delivery=False).filter(shipped=False).filter(country="Espanya").filter(count__in=[4, 5, 6])
        context['es_4'] = Order.objects.filter(deleted=False).filter(made=True).filter(hand_delivery=False).filter(shipped=False).filter(country="Espanya").filter(count__gt=6)
        context['eu_1'] = Order.objects.filter(deleted=False).filter(made=True).filter(hand_delivery=False).filter(shipped=False).exclude(country="Espanya").filter(count=1)
        context['eu_2'] = Order.objects.filter(deleted=False).filter(made=True).filter(hand_delivery=False).filter(shipped=False).exclude(country="Espanya").filter(count__in=[2, 3])
        context['eu_3'] = Order.objects.filter(deleted=False).filter(made=True).filter(hand_delivery=False).filter(shipped=False).exclude(country="Espanya").filter(count__in=[4, 5, 6])
        context['eu_4'] = Order.objects.filter(deleted=False).filter(made=True).filter(hand_delivery=False).filter(shipped=False).exclude(country="Espanya").filter(count__gt=6)
        context['data'] = ProjectSettings.objects.values('name', 'company', 'address', 'cp', 'town', 'country', 'logo_font').get()
        return context


class StaffInvoiceListView(ListView):

    template_name = 'staff/invoice_list.html'
    context_object_name = 'invoice_list'

    def dispatch(self, *args, **kwargs):
        try:
            invoice = Invoice.objects.all()[:1]
            if invoice.id < 164:
                invoice.create_handmade()
        except:
            pass
        return super(StaffInvoiceListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        '''test_user = get_object_or_404(InoxUser, email='13.oriol@gmail.com')
        invoice_list = Invoice.objects.all().exclude(user=test_user)'''
        invoice_list = Invoice.objects.all()
        for invoice in invoice_list:
            try:
                invoice.invoice_rect = invoice.rectinvoice_set.get()
            except:
                invoice.invoice_rect = None
        return invoice_list


class StaffRectInvoiceListView(ListView):

    template_name = 'staff/rect_invoice_list.html'
    context_object_name = 'invoice_list'
    model = RectInvoice


class StaffInvoiceRectificateView(RedirectView):

    url = reverse_lazy('staff_invoice_list')

    def dispatch(self, *args, **kwargs):
        invoice = get_object_or_404(Invoice, pk=self.kwargs.get('pk'))
        invoice.rectificate()
        return super(StaffInvoiceRectificateView, self).dispatch(*args, **kwargs)


class StaffOrderListGenerateInvoiceView(ListView):

    template_name = 'staff/order_list_generate_invoice.html'
    context_object_name = 'order_list'
    queryset = Order.objects.filter(deleted=False).filter(made=True)


class StaffInvoiceFromOrderView(RedirectView):

    url = reverse_lazy('staff_order_list_create_invoice')

    def dispatch(self, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        order.invoice = Invoice.objects.create(
            user=order.user,
            order=order,
            price=order.price,
            iva=Decimal(str(order.iva)),
        )
        order.save()
        return super(StaffInvoiceFromOrderView, self).dispatch(*args, **kwargs)


class StaffInvoiceCreateView(CreateView):

    template_name = 'staff/invoice_create.html'
    form_class = StaffInvoiceCreateForm
    model = Invoice
    success_url = reverse_lazy('staff_invoice_list')


class StaffOrderDetailPdfView(RenderPDF, DetailView):

    template_name = 'pdf/order_pdf.html'
    context_object_name = 'order'

    def get_object(self):
        object = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        object.data = ProjectSettings.objects.values('name', 'company', 'tax_code', 'invoice_address', 'invoice_cp', 'invoice_town', 'invoice_country', 'logo_font', 'phone', 'email').get()
        #object.tags = object.tags()
        return object


class StaffInvoiceDetailPdfView(RenderPDF, DetailView):

    template_name = 'pdf/invoice_pdf.html'
    context_object_name = 'invoice'

    def get_object(self):
        object = get_object_or_404(Invoice, pk=self.kwargs.get('pk'))
        try:
            object.tags = object.order.tags()
        except:
            pass
        object.data = ProjectSettings.objects.values('name', 'company', 'tax_code', 'invoice_address', 'invoice_cp', 'invoice_town', 'invoice_country', 'logo_font', 'phone', 'email').get()
        return object


class StaffRectInvoiceDetailPdfView(RenderPDF, DetailView):

    template_name = 'pdf/invoice_rect_pdf.html'
    context_object_name = 'invoice'

    def get_object(self):
        object = get_object_or_404(RectInvoice, pk=self.kwargs.get('pk'))
        object.data = ProjectSettings.objects.values('name', 'company', 'tax_code', 'invoice_address', 'invoice_cp', 'invoice_town', 'invoice_country', 'logo_font', 'phone', 'email').get()
        return object
