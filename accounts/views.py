#-*- coding:utf-8 -*-
"""
Custom registration views to use with django-registration
and a custom user model.
"""

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView, FormView
from django.views.generic import TemplateView
from django.utils.translation import check_for_language
from django.utils.http import is_safe_url
from django import http

from registration.views import _RequestPassingFormView
from registration import signals

from .forms import (
    CustomRegistrationForm,
    ShippingDataForm,
    InvoiceDataForm,
    ProfessionalDataForm,
)
from .models import InoxUser


class CustomBaseRegistrationView(_RequestPassingFormView):
    # Custom base class for user registration views.
    disallowed_url = 'registration_disallowed'
    form_class = CustomRegistrationForm
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    success_url = "/accounts/"
    template_name = 'registration/registration_form.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Check that user signup is allowed before even bothering to
        dispatch or do other processing.
        """
        if not self.registration_allowed(request):
            return redirect(self.disallowed_url)
        return super(CustomBaseRegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, request, form):
        new_user = self.register(request, **form.cleaned_data)
        success_url = self.get_success_url(request, new_user)

        """
        success_url may be a simple string, or a tuple providing
        the full argument set for redirect(). Attempting to unpack
        it tells us which one it is.
        """
        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(success_url)

    def registration_allowed(self, request):
        """
        Override this to enable/disable user registration, either
        globally or on a per-request basis.

        """
        return True

    def register(self, request, **cleaned_data):
        """
        Implement user-registration logic here. Access to both the
        request and the full cleaned_data of the registration form is
        available here.

        """
        raise NotImplementedError


class CustomRegistrationView(CustomBaseRegistrationView):
    """
    Custom view for the simple registration backend from django-registration,
    to be used with a custom user model which only needs an email an password
    to register, and is immediately signed up and logged in.
    """

    def register(self, request, **cleaned_data):
        email, password = cleaned_data['email'], cleaned_data['password1']
        InoxUser.objects.create_user(email, password)

        new_user = authenticate(email=email, password=password)
        login(request, new_user)
        signals.user_registered.send(sender=self.__class__, user=new_user, request=request)

        new_user.lang = request.LANGUAGE_CODE
        new_user.save()
        return new_user

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:
            * if ``REGISTRATION_OPEN`` is not spacified in settings, or is
            set to ``True``, registration is permitted.
            * if ``REGISTRATION_OPEN`` is both specified and set to
            ``False``, registration is not permitted.
        """

        return getattr(settings, 'REGISTRATION_OPEN', True)

    #def get_success_url(self, request, user):
        #return (user.get_absolute_url(), (), {})


class ShippingDataUpdateView(UpdateView):

    User = get_user_model()

    template_name = 'accounts/update_data.html'
    form_class = ShippingDataForm
    success_url = "/accounts/"
    model = User

    def get(self, request, **kwargs):
        try:
            self.object = InoxUser.objects.get(name=self.request.user)
        except:
            self.object = InoxUser.objects.get(email=self.request.user)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ShippingDataUpdateView, self).get_context_data(**kwargs)
        # Add in the extra context
        context['title'] = _("Shipping data")
        return context

    def form_valid(self, form):
        """
        This method is called when valid form data has been POSTed.
        It should return an HttpResponse.
        """
        form.save()
        return super(ShippingDataUpdateView, self).form_valid(form)


class InvoiceDataUpdateView(UpdateView):

    User = get_user_model()

    template_name = 'accounts/update_invoice_data.html'
    form_class = InvoiceDataForm
    success_url = "/accounts/"
    model = User

    def get(self, request, **kwargs):
        try:
            self.object = InoxUser.objects.get(name=self.request.user)
        except:
            self.object = InoxUser.objects.get(email=self.request.user)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InvoiceDataUpdateView, self).get_context_data(**kwargs)
        # Add in the extra context
        context['title'] = _("Invoice data")
        return context

    def form_valid(self, form):
        """
        This method is called when valid form data has been POSTed.
        It should return an HttpResponse.
        """
        form.save()
        if self.object.same_address_for_invoice:
            self.object.invoice_address = self.object.shipping_address
            self.object.invoice_code = self.object.shipping_code
            self.object.invoice_town = self.object.shipping_town
        self.object.save()
        return super(InvoiceDataUpdateView, self).form_valid(form)


class ProfessionalDataUpdateView(UpdateView):

    User = get_user_model()

    template_name = 'accounts/update_data.html'
    form_class = ProfessionalDataForm
    success_url = "/accounts/"
    model = User

    def get(self, request, **kwargs):
        try:
            self.object = InoxUser.objects.get(name=self.request.user)
        except:
            self.object = InoxUser.objects.get(email=self.request.user)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProfessionalDataUpdateView, self).get_context_data(**kwargs)
        # Add in the extra context
        context['title'] = _("Professional data")
        return context

    def form_valid(self, form):
        """
        This method is called when valid form data has been POSTed.
        It should return an HttpResponse.
        """
        form.save()
        return super(ProfessionalDataUpdateView, self).form_valid(form)


class UserDetailView(TemplateView):

    template_name = 'accounts/main.html'


def set_language(request):

    """
    Set_language view from Django.
    Redirect to a given url while setting the chosen language in the
    session or cookie. The url and the language code need to be
    specified in the request parameters.
    Since this view changes how the user will see the rest of the site, it must
    only be accessed as a POST request. If called as a GET request, it will
    redirect to the page in the request (the 'next' parameter) without changing
    any state.
    """

    next = request.POST.get('next', request.GET.get('next'))
    if not is_safe_url(url=next, host=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=next, host=request.get_host()):
            next = '/'
    response = http.HttpResponseRedirect(next)
    if request.method == 'POST':
        lang_code = request.POST.get('language', None)
        try:
            user = get_object_or_404(InoxUser, email=request.user)
            if user.is_authenticated:
                user.lang = lang_code
                user.save()
        except:
            pass
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response


def cookies_agreement_view(request):
    next = request.POST.get('next', request.GET.get('next'))
    if not is_safe_url(url=next, host=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=next, host=request.get_host()):
            next = '/'
    if request.method == 'POST':
        request.session['COOKIES_AGREEMENT'] = 'accepted'
    return http.HttpResponseRedirect(next)
