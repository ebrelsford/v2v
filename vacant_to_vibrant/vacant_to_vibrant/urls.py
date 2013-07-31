from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from api.api import v1_api
import external_data_sync
import autocomplete_light

autocomplete_light.autodiscover()

admin.autodiscover()
external_data_sync.autodiscover()

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,
                     show_indexes=True)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
    url(r'^lots/', include('lots.urls', 'lots')),
    url(r'^places/', include('inplace.urls', 'inplace')),
    url(r'^parcels/', include('phillydata.parcels.urls', 'parcels')),

    url(r'^extraadmin/', include('extraadmin.urls', 'extraadmin')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),

    url(r'^forms/', include('forms_builder.forms.urls')),
    url(r'^survey/', include('survey.urls')),

    url('^activity/', include('actstream.urls')),
    url('^activity-stream/', include('inplace_activity_stream.urls')),

    url(r'^api/', include(v1_api.urls)),

    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^djangojs/', include('djangojs.urls')),
    url(r'^report_builder/', include('report_builder.urls')),

    url(r'', include('feincms.urls')),
)
