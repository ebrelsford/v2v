from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)

urlpatterns += staticfiles_urlpatterns()

urlpatterns = patterns('',
    url(r'^contact/', include('contact.urls', 'contact_form')),
    url(r'^lots/', include('lots.urls', 'lots')),
    url(r'^places/', include('inplace.urls', 'inplace')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    #
    # fiber
    #
    (r'^api/v2/', include('fiber.rest_api.urls')),
    (r'^admin/fiber/', include('fiber.admin_urls')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': ('fiber',),}),

    (r'', 'fiber.views.page'),
)
