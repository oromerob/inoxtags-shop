#-*- coding:utf-8 -*-

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from autoslug import AutoSlugField
from transmeta import TransMeta

from apps.settings.models import Country


class PartnerZone(models.Model):
    country = models.ForeignKey(Country)
    zone = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='zone')

    def __unicode__(self):
        return self.zone


class PartnerTown(models.Model):
    zone = models.ForeignKey(PartnerZone)
    town = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='town')

    def __unicode__(self):
        return self.town


class InoxUserManager(BaseUserManager):


    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email,is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)


    def create_superuser(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class InoxUser(AbstractBaseUser,PermissionsMixin):

    LANGUAGES = settings.LANGUAGES
    COUNTRIES = settings.COUNTRIES

    email = models.EmailField(max_length=255,unique=True,db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    lang = models.CharField(max_length=100, choices=LANGUAGES)
    #Name and shipping address required when registering
    name = models.CharField(
        max_length=255,
        verbose_name=_("full name or company's name"),
        blank=True,
        null=True
    )
    shipping_address = models.CharField(
        max_length=255,
        verbose_name=_('shipping address'),
        blank=True,
        null=True
    )
    shipping_code = models.CharField(
        max_length=5,
        verbose_name=_('postal code'),
        blank=True,
        null=True
    )
    shipping_town = models.CharField(
        max_length=200,
        verbose_name=_('town'),
        blank=True,
        null=True
    )
    shipping_country = models.ForeignKey(
        Country,
        verbose_name=_('country'),
        blank=True,
        null=True,
    )
    #Invoice optional data
    same_address_for_invoice = models.BooleanField(
        default=True,
        verbose_name=_('use the same address for the invoice')
    )
    invoice_name = models.CharField(
        max_length=255,
        verbose_name=_('legal name'),
        blank=True,
        null=True
    )
    invoice_tax_code = models.CharField(
        max_length=50,
        verbose_name=_('tax code'),
        blank=True,
        null=True
    )
    invoice_extra_charge = models.BooleanField(
        default=False,
        verbose_name=_('extra charge for equivalence only for spanish professional customers')
    )
    invoice_address = models.CharField(
        max_length=255,
        verbose_name=_('legal address'),
        blank=True,
        null=True
    )
    invoice_code = models.CharField(
        max_length=5,
        verbose_name=_('postal code'),
        blank=True,
        null=True
    )
    invoice_town = models.CharField(
        max_length=200,
        verbose_name=_('town'),
        blank=True,
        null=True
    )
    #Professional optional data
    is_professional = models.BooleanField(
        default=False,
        verbose_name=_('is professional')
    )
    share = models.BooleanField(
        _('share professional customer data'),
        default=False
    )
    phone_1 = models.CharField(
        max_length=15,
        verbose_name=_('main phone number'),
        blank=True,
        null=True
    )
    phone_2 = models.CharField(
        max_length=15,
        verbose_name=_('alternative phone number'),
        blank=True,
        null=True
    )
    website = models.URLField(
        max_length=255,
        blank=True,
        null=True
    )
    #zone = models.ForeignKey(PartnerZone,blank=True,null=True)
    town = models.ForeignKey(PartnerTown,blank=True,null=True)
    #Shipping and payment options for professional clients
    hand_delivery = models.BooleanField(
        default=False,
        verbose_name='entrega en mà'
    )
    money_order = models.BooleanField(
        default=False,
        verbose_name='pagament en gir bancari'
    )
    bank_wire = models.BooleanField(
        default=False,
        verbose_name='pagament per transferència (post-pagament)'
    )
    old_client = models.BooleanField(
        default=False,
        verbose_name='client antic (amb una altra relació de preus)'
    )

    objects = InoxUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
