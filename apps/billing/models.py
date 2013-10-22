#-*- coding:utf-8 -*-
from django.db import models
from django.conf import settings
from decimal import Decimal

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from apps.shop.models import Cart, Product, Color


class Iva(models.Model):
    iva = models.DecimalField(max_digits=4, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % (self.iva)


class Order(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    cart = models.ForeignKey(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # Shipment data
    to = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=8)
    town = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    # Price and weight data
    price = models.DecimalField(max_digits=6, decimal_places=2)
    count = models.PositiveIntegerField(blank=True)
    iva = models.DecimalField(max_digits=4, decimal_places=2)
    # Process indicators
    payed = models.BooleanField(default=False, verbose_name="Pagat")
    hand_delivery = models.BooleanField(default=False)
    made = models.BooleanField(default=False)
    ship_date = models.DateTimeField(blank=True, null=True)
    shipped = models.BooleanField(default=False)
    shipping_code = models.CharField(max_length=100, blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s / %s' % (self.creation_date.year, self.id)

    def update_shipment_data(self):
        if self.user.name:
            self.to = self.user.name
        else:
            self.mark_as_deleted()
            return
        if self.user.shipping_address:
            self.address = self.user.shipping_address
        else:
            self.mark_as_deleted()
            return
        if self.user.shipping_code:
            self.postal_code = self.user.shipping_code
        else:
            self.mark_as_deleted()
            return
        if self.user.shipping_town:
            self.town = self.user.shipping_town
        else:
            self.mark_as_deleted()
            return
        if self.user.shipping_country:
            self.country = self.user.shipping_country.country
        else:
            self.mark_as_deleted()
        self.save()
        return


    def check_made(self):
        if not self.orderitem_set.filter(made=False).exists():
            self.made = True
            self.save()
        return

    def update_count(self):
        result = 0
        for item in self.orderitem_set.all():
            result += item.quantity
        self.count = result
        self.save()
        return result

    def delete_items(self):
        for item in self.orderitem_set.all():
            item.delete()
        return

    def mark_as_deleted(self):
        self.delete_items()
        self.deleted = True
        self.save()

        # Sending the confirmation email

        mail = self.user.email
        try:
            if self.user.lang == "ca":
                subject = "Comanda anul.lada a INOXtags.com"
                html_content = render_to_string('email/order_deleted_ca.html', {'order': self})
            elif self.user.lang == "es":
                subject = "Pedido anulado en INOXtags.com"
                html_content = render_to_string('email/order_deleted_es.html', {'order': self})
            else:
                subject = "Order deleted in INOXtags.com"
                html_content = render_to_string('email/order_deleted_en.html', {'order': self})
        except:
            subject = "Order deleted in INOXtags.com"
            html_content = render_to_string('email/order_deleted_en.html', {'order': self})
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, to=[mail])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # Create the rectificative invoice if needed

        if self.invoice():
            self.invoice().rectificate()

        return

    def invoice(self):
        try:
            invoice = self.invoice_set.get(rect=False)
        except:
            invoice = None
        return invoice

    def count_items(self):
        result = 0
        for item in self.orderitem_set.all():
            if not item.repetition:
                result += item.quantity
        return result

    def update_price(self):
        result = 0
        count = self.count_items()
        if self.user.is_professional:
            if count >= 4:
                for item in self.orderitem_set.all():
                    if not item.repetition:
                        result += item.price_special_4 * item.quantity
            elif count == 3:
                for item in self.orderitem_set.all():
                    if not item.repetition:
                        result += item.price_special_3 * item.quantity
            elif count == 2:
                for item in self.orderitem_set.all():
                    if not item.repetition:
                        result += item.price_special_2 * item.quantity
            else:
                for item in self.orderitem_set.all():
                    if not item.repetition:
                        result += item.price_special_1 * item.quantity
        else:
            for item in self.orderitem_set.all():
                if not item.repetition:
                    result += item.price * item.quantity
        return result

    def modify(self):
        self.count = self.update_count()
        self.price = self.update_price()
        self.save()

        # Send mail notifying the modifyed order

        mail = self.user.email
        try:
            if self.user.lang == "ca":
                subject = "Comanda modificada a INOXtags.com"
                html_content = render_to_string('email/order_modified_ca.html',{'order':self})
            elif self.user.lang == "es":
                subject = "Pedido modificado en INOXtags.com"
                html_content = render_to_string('email/order_modified_es.html',{'order':self})
            else:
                subject = "Order modified in INOXtags.com"
                html_content = render_to_string('email/order_modified_en.html',{'order':self})
        except:
            subject = "Order modified in INOXtags.com"
            html_content = render_to_string('email/order_modified_en.html',{'order':self})
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, to=[mail])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # if invoice exists creates a rectificative invoice

        if self.invoice():
            self.invoice().rectificate()
        return

    def mark_as_payed(self):
        self.payed = True
        self.save()
        return

    def tags(self):
        items = self.orderitem_set.all()
        return items

    class Meta:
        ordering = ('-creation_date',)


class OrderItem(models.Model):

    QUANTITY_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    order = models.ForeignKey(Order, verbose_name="Comanda")
    quantity = models.PositiveIntegerField(verbose_name='quantitat', choices=QUANTITY_CHOICES)
    product = models.ForeignKey(Product, verbose_name="producte")
    color = models.ForeignKey(Color, blank=True, null=True)
    front_main = models.CharField(max_length=15, verbose_name="frontal principal")
    front_tel = models.CharField(max_length=15, blank=True, verbose_name="frontal telèfon")
    back_1 = models.CharField(max_length=15, blank=True, verbose_name="revers 1")
    back_2 = models.CharField(max_length=15, blank=True, verbose_name="revers 2")
    back_3 = models.CharField(max_length=15, blank=True, verbose_name="revers 3")
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='preu per particulars')
    price_special_1 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='preu per professionals (una placa)')
    price_special_2 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='preu per professionals (dues plaques)')
    price_special_3 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='preu per professionals (tres plaques)')
    price_special_4 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='preu per professionals (més de tres plaques)')
    price_in_hand = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='hand delivery price')
    made = models.BooleanField(default=False)
    repetition = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % (self.id)


class Invoice(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    order = models.ForeignKey(Order, null=True, blank=True)
    concept = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=2)
    rect = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s / %s' % (self.creation_date.year, self.id)

    def rectificate(self):
        RectInvoice.objects.create(
            user=self.user,
            invoice=self,
            price=self.price,
            iva=Decimal(str(self.iva)),
        )
        self.rect = True
        self.save()
        return

    def price_base(self):
        return self.price / (1 + (self.iva / 100))

    def price_iva(self):
        return self.price - self.price_base()

    class Meta:
        ordering = ('-creation_date',)


class RectInvoice(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    invoice = models.ForeignKey(Invoice)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=2)

    def __unicode__(self):
        return u'Rect. %s / %s' % (self.creation_date.year, self.id)

    def price_base(self):
        return self.price / (1 + (self.iva / 100))

    def price_iva(self):
        return self.price - self.price_base()

    class Meta:
        ordering = ('-creation_date',)


