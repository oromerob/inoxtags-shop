#-*- coding:utf-8 -*-
"""
Custom forms and validation code for custom user registration
"""

from django import forms
from django.utils.translation import ugettext_lazy as _

from accounts.models import InoxUser


class CustomRegistrationForm(forms.Form):
    """
    Custom registration form for custom user made from
    django-registration forms to be used with the
    django-registration app.
    """

    required_css_class = 'required'

    email = forms.EmailField(label=_("E-mail"))
    password1 = forms.CharField(widget=forms.PasswordInput, label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_("Password (again)"))

    tos = forms.BooleanField(widget=forms.CheckboxInput, label=_(u'I have read and agree to the Terms of Service'), error_messages={'required': _("You must agree to the terms to register")})

    def clean_email(self):
        """
        Valideate that teh supplied email address is unique for the site
        """
        if InoxUser.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']

    def clean(self):
        """
        Verify that the values entered into the two password fields match.
        Note thet an error here will end up in ``non_field_errors()``
        because it doesn't apply to a single field.
        """

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


class ShippingDataForm(forms.ModelForm):

    class Meta:
        model = InoxUser
        fields = ('name', 'shipping_address', 'shipping_code', 'shipping_town', 'shipping_country',)


class InvoiceDataForm(forms.ModelForm):

    class Meta:
        model = InoxUser
        fields = ('invoice_name', 'invoice_tax_code', 'invoice_address', 'invoice_code', 'invoice_town',)


class ProfessionalDataForm(forms.ModelForm):

    class Meta:
        model = InoxUser
        fields = ('phone_1', 'phone_2', 'website',)
