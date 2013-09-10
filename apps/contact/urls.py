from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from apps.contact.views import ContactFormView

urlpatterns = patterns('',
    url(r'^$', ContactFormView.as_view(), name='contact_form'),
    url(r'^success/$', TemplateView.as_view(template_name='contact/contact_success.html')),
)
