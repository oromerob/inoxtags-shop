from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'', include('apps.content_pages.urls')),
    url(r'^contact/', include('apps.contact.urls')),
    url(r'^shop/', include('apps.shop.urls')),
    url(r'', include('apps.checkout.urls')),
    url(r'^find_us/', include('apps.partners.urls')),
    url(r'^staff/', include('apps.staff.urls')),
    url(r'zebra/', include('zebra.urls', namespace="zebra", app_name='zebra')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, }
        ),
    )
