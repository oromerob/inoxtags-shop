#-*- coding:utf-8 -*-
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import InoxUser, Country, PartnerZone, PartnerTown

class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = InoxUser
        exclude = ['is_active','is_staff','date_joined']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on the user, but replaces the password field with admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = InoxUser

    def clean_password(self):
        """
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the field does not have access to the initial value.
        """
        return self.initial["password"]


class InoxUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    """
    The fields to be used in displaying the User Model.
    These override the definitions on the base UserAdmin that reference specific fields on auth.User.
    """
    list_display = ('email','name','shipping_address','shipping_code','shipping_town','shipping_country')
    list_filter = ('shipping_country',)
    fieldsets = (
        (None, {'fields': ('email','password','lang')}),
        ('Name', {'fields': ('name',)}),
        ('Basic permissions', {'fields': ('is_active','is_staff','is_superuser')}),
        ('Shipping address', {'fields': ('shipping_address','shipping_code','shipping_town','shipping_country')}),
        ('Invoice data', {'fields': ('invoice_required','invoice_name','invoice_tax_code','invoice_extra_charge','invoice_address','invoice_code','invoice_town')}),
        ('Specific professional data', {'fields': ('is_professional','hand_delivery','order_money','share','phone_1','phone_2','website','zone','town')}),
        ('Extended permissions', {'fields': ('groups','user_permissions')}),
        ('Important dates', {'fields': ('last_login','date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('-id',)
    filter_horizontal = ()


admin.site.register(InoxUser, InoxUserAdmin)
admin.site.register(Country)
admin.site.register(PartnerTown)
admin.site.register(PartnerZone)
