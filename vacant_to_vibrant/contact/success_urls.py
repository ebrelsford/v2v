from django.conf.urls.defaults import patterns, url

from .views import ContactCompleted

urlpatterns = patterns('',
    url('^$', ContactCompleted.as_view(), name='completed'),
)
