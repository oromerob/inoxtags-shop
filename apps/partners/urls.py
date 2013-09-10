from django.conf.urls import patterns, include, url

from apps.partners.views import PartnerListView, PartnerDetailView, PartnerMainView


urlpatterns = patterns('',
    url(r'^$', PartnerMainView.as_view(), name='partner_main'),
    url(r'^(?P<slug>[-\w]+)/$', PartnerListView.as_view(), name='partner_list'),
    url(r'^detail/(?P<pk>\d+)/$', PartnerDetailView.as_view(), name='partner_detail'),
)
