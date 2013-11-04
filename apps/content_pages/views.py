#-*- coding:utf-8 -*-
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext_lazy as _

from .models import HomeSlider, HomeFeaturette, AboutPage
from apps.settings.models import Tos


class HomePageView(TemplateView):

    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['sliders'] = HomeSlider.objects.filter(is_active=True)
        context['featurettes'] = HomeFeaturette.objects.filter(is_active=True)
        return context


class AboutPageView(TemplateView):

    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutPageView, self).get_context_data(**kwargs)
        try:
            content = AboutPage.objects.filter(active=True).get()
        except:
            content = None
        context['content'] = content
        return context


class TermsPageView(TemplateView):

    template_name = 'pages/terms.html'

    def get_context_data(self, **kwargs):
        context = super(TermsPageView, self).get_context_data(**kwargs)
        tos = Tos.objects.get()
        context['text'] = tos.terms
        return context


class PrivacyPageView(TemplateView):

    template_name = 'pages/terms.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyPageView, self).get_context_data(**kwargs)
        tos = Tos.objects.get()
        context['text'] = tos.privacity
        return context
