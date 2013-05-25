from django.conf.urls.defaults import patterns, url

from .views import ExtraAdminIndex


urlpatterns = patterns('',
    url(r'^$', ExtraAdminIndex.as_view()),
)
