from django.conf.urls.defaults import patterns, url

from .views import ContactFormView, ContactCompleted


urlpatterns = patterns('',
    url('^$', ContactFormView.as_view(), name='form'),
    url('^success/$', ContactCompleted.as_view(), name='completed'),
)
