from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from apps.backend_bank_transfer.views import BankTransferView


urlpatterns = patterns('',
    url(r'^payment/bank_transfer/$', login_required(BankTransferView.as_view()), name='bank_transfer'),
)
