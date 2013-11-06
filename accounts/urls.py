from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from accounts.views import (
    CustomRegistrationView,
    ShippingDataUpdateView,
    InvoiceDataUpdateView,
    ProfessionalDataUpdateView,
    UserDetailView,
)

urlpatterns = patterns('',
    url(r'^$', login_required(UserDetailView.as_view()), name='inox_user_detail'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^register/$', CustomRegistrationView.as_view(), name='registration_register'),
    url(r'^shipping_data/$', login_required(ShippingDataUpdateView.as_view()), name='shipping_data_update'),
    url(r'^invoice_data/$', login_required(InvoiceDataUpdateView.as_view()), name='invoice_data_update'),
    url(r'^professional_data/$', login_required(ProfessionalDataUpdateView.as_view()), name='professional_data_update'),
    url(r'^setlang/$', 'accounts.views.set_language', name='user_set_language'),
    url(r'^cookies/$', 'accounts.views.cookies_agreement_view', name='cookies_agreement'),
)
