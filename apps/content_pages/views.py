#-*- coding:utf-8 -*-
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext_lazy as _

from apps.content_pages.models import HomeSlider, HomeFeaturette
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


class TermsPageView(TemplateView):

    template_name = 'pages/terms.html'

    def get_context_data(self, **kwargs):
        context = super(TermsPageView, self).get_context_data(**kwargs)
        context['text'] = Tos.objects.values("terms").get()
        return context


class PrivacyPageView(TemplateView):

    template_name = 'pages/terms.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyPageView, self).get_context_data(**kwargs)
        context['text'] = Tos.objects.values("privacity").get()
        return context
