#-*- coding:utf-8 -*-
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404

from accounts.models import InoxUser, PartnerZone


class PartnerMainView(TemplateView):

    template_name = 'partners/partner_main.html'

    def get_context_data(self, **kwargs):
        context = super(PartnerMainView, self).get_context_data(**kwargs)
        context['nav_list'] = PartnerZone.objects.all().order_by('country')
        return context


class PartnerListView(ListView):

    template_name = 'partners/partner_list.html'
    context_object_name = 'partner_list'

    def get_queryset(self):
        zone = get_object_or_404(PartnerZone, slug=self.kwargs.get('slug'))
        return InoxUser.objects.filter(share=True).filter(zone=zone).order_by('shipping_town')

    def get_context_data(self, **kwargs):
        context = super(PartnerListView, self).get_context_data(**kwargs)
        context['nav_list'] = PartnerZone.objects.all().order_by('country')
        return context


class PartnerDetailView(DetailView):

    template_name = 'partners/partner_detail.html'
    queryset = InoxUser.objects.filter(share=True)
    context_object_name = 'partner'

    def get_context_data(self, **kwargs):
        context = super(PartnerDetailView, self).get_context_data(**kwargs)
        context['nav_list'] = PartnerZone.objects.all().order_by('country')
        context['address'] = self.object.shipping_address + ' ' + self.object.shipping_code + ' ' + self.object.shipping_town + ' ' + self.object.shipping_country.country
        return context
