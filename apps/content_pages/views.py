#-*- coding:utf-8 -*-
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext_lazy as _

from .models import HomeSlider, HomeFeaturette, StaticPage


class HomePageView(TemplateView):

    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['sliders'] = HomeSlider.objects.filter(is_active=True)
        context['featurettes'] = HomeFeaturette.objects.filter(is_active=True)
        return context


class TermsPageView(TemplateView):

    template_name = 'pages/static_page.html'

    def get_context_data(self, **kwargs):
        context = super(TermsPageView, self).get_context_data(**kwargs)
        try:
            context['page'] = StaticPage.objects.filter(name='terms').get()
        except:
            pass
        return context


class PrivacyPageView(TemplateView):

    template_name = 'pages/static_page.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyPageView, self).get_context_data(**kwargs)
        try:
            context['page'] = StaticPage.objects.filter(name='privacy').get()
        except:
            pass
        return context


class CookiesPageView(TemplateView):

    template_name = 'pages/static_page.html'

    def get_context_data(self, **kwargs):
        context = super(CookiesPageView, self).get_context_data(**kwargs)
        try:
            context['page'] = StaticPage.objects.filter(name='cookies').get()
        except:
            pass
        return context


class AboutPageView(TemplateView):

    template_name = 'pages/static_page.html'

    def get_context_data(self, **kwargs):
        context = super(AboutPageView, self).get_context_data(**kwargs)
        try:
            context['page'] = StaticPage.objects.filter(name='about').get()
        except:
            pass
        return context
