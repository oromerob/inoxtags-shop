#-*- coding:utf-8 -*-
"""
Custom registration views to use with django-registration
and a custom user model.
"""

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView

from registration.views import _RequestPassingFormView
from registration import signals

from accounts.forms import CustomRegistrationForm, ShippingDataForm, InvoiceDataForm, ProfessionalDataForm
from accounts.models import InoxUser


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

    template_name = 'accounts/update_data.html'
    form_class = InvoiceDataForm
    success_url = "/accounts/"
    model = User

    def get(self, request, **kwargs):
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
        return super(InvoiceDataUpdateView, self).form_valid(form)


class ProfessionalDataUpdateView(UpdateView):

    User = get_user_model()

    template_name = 'accounts/update_data.html'
    form_class = ProfessionalDataForm
    success_url = "/accounts/"
    model = User

    def get(self, request, **kwargs):
        self.object = InoxUser.objects.filter(is_professional=True).get(email=self.request.user)
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

