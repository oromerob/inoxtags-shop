#-*- coding:utf-8 -*-
import datetime
from decimal import Decimal
from django.db import models
from django.utils.translation import ugettext as _

from autoslug import AutoSlugField
from transmeta import TransMeta


class Iva(models.Model):
    iva = models.DecimalField(max_digits=4, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % (self.iva)


class Shipping(models.Model):
    es = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Enviaments a Espanya')
    eu = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Enviaments a Europa')

    def __unicode__(self):
        return unicode(self.es)

    def es_base(self):
        iva = Iva.objects.get()
        return self.es / (1 + (Decimal(str(iva)) / 100))

    def eu_base(self):
        iva = Iva.objects.get()
        return self.eu / (1 + (Decimal(str(iva)) / 100))


class Category(models.Model):
    __metaclass__ = TransMeta

    category = models.CharField(max_length=50, verbose_name=_("Category"))
    slug = AutoSlugField(max_length=100, unique=True, populate_from='category')
    img = models.ImageField(upload_to="product/img/", blank=True, verbose_name=_("Image"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    # product's price depends on the category
    price_normal = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='preu per particulars')
    price_prof = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='preu per professionals')
    price_in_hand = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='preu per professionals, entrega en mà')
    has_color = models.BooleanField(default=False)
    has_front_main = models.BooleanField(default=False)
    has_front_tel = models.BooleanField(default=False)
    has_back_1 = models.BooleanField(default=False)
    has_back_2 = models.BooleanField(default=False)
    has_back_3 = models.BooleanField(default=False)

    def price_initial_es(self):
        shipping = Shipping.objects.get()
        return self.price_prof + shipping.es

    def price_initial_eu(self):
        shipping = Shipping.objects.get()
        return self.price_prof + shipping.eu

    def __unicode__(self):
        return self.category

    class Meta:
        verbose_name_plural = "Categories"
        translate = ('category', 'description',)


class Shape(models.Model):
    __metaclass__ = TransMeta

    shape = models.CharField(max_length=100, verbose_name=_("Shape"))

    class Meta:
        translate = ('shape',)

    def __unicode__(self):
        return self.shape


class Color(models.Model):
    __metaclass__ = TransMeta

    color = models.CharField(max_length=20, verbose_name=_("Color"))

    class Meta:
        translate = ('color',)

    def __unicode__(self):
        return self.color


class Product(models.Model):
    __metaclass__ = TransMeta

    # Base product to customize in the shop
    category = models.ForeignKey(Category)
    shape = models.ForeignKey(Shape)
    slug = AutoSlugField(max_length=100, populate_from='name')
    img_1 = models.ImageField(upload_to="img/", verbose_name="imatge principal")
    img_2 = models.ImageField(upload_to="img/", verbose_name="imatge combinada (davant i darrera)", blank=True)
    img_3 = models.ImageField(upload_to="img/", verbose_name="imatge acotada amb mides", blank=True)
    description = models.TextField(verbose_name=_("Description"))

    def __unicode__(self):
        return u"%s %s" % (self.category, self.shape)

    def name(self):
        return u"%s %s" % (self.category, self.shape)

    class Meta:
        verbose_name_plural = "Products"
        ordering = ['category']
        translate = ('description',)


class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name='creation date', auto_now_add=True)
    checked_out = models.BooleanField(default=False, verbose_name="checked out")

    def __unicode__(self):
        return unicode(self.id)

    def get_count(self):
        result = 0
        for item in self.customproduct_set.all():
            if not item.repetition:
                result += item.quantity
        return result

    def get_count_total(self):
        result = 0
        for item in self.customproduct_set.all():
            result += item.quantity
        return result

    def get_price(self, user):
        result = 0
        count = self.get_count()
        shipping = Shipping.objects.get()
        if user.is_professional:
            if not user.hand_delivery:
                if user.shipping_country.country == 'Espanya':
                    result += shipping.es
                else:
                    result += shipping.eu
                for item in self.customproduct_set.all():
                    if not item.repetition:
                        result += item.price_prof * item.quantity
            else:
                for item in self.customproduct_set.all():
                    if not item.repetition:
                        result += item.price_in_hand * item.quantity
        else:
            for item in self.customproduct_set.all():
                if not item.repetition:
                    result += item.price_normal * item.quantity
        return result

    class Meta:
        ordering = ('-creation_date',)


class CustomProduct(models.Model):
    # Customizable product displayed in the shop.

    QUANTITY_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    cart = models.ForeignKey(Cart)
    quantity = models.PositiveIntegerField(verbose_name='quantitat', choices=QUANTITY_CHOICES)
    product = models.ForeignKey(Product)
    # Product costumisation
    color = models.ForeignKey(Color, blank=True, null=True)
    front_main = models.CharField(max_length=15, blank=True, verbose_name="frontal principal")
    front_tel = models.CharField(max_length=15, blank=True, verbose_name="frontal telèfon")
    back_1 = models.CharField(max_length=15, blank=True, verbose_name="revers 1")
    back_2 = models.CharField(max_length=15, blank=True, verbose_name="revers 2")
    back_3 = models.CharField(max_length=15, blank=True, verbose_name="revers 3")
    # inherits prices from category
    price_normal = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='preu per particulars')
    price_prof = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='preu per professionals')
    price_in_hand = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='preu per professionals, entrega en mà')
    # internal fields
    made = models.BooleanField(default=False)
    repetition = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.id)

    class Meta:
        verbose_name_plural = "Custom products"
