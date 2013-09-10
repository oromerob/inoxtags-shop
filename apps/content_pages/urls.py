from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from apps.content_pages.views import HomePageView, AboutPageView, TermsPageView, PrivacyPageView


urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home_page'),
    url(r'^about/$', AboutPageView.as_view(), name='about_page'),
    url(r'^terms/$', TermsPageView.as_view(), name='terms_page'),
    url(r'^privacy/$', PrivacyPageView.as_view(), name='privacy_page'),
)
