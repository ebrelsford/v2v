from django.conf.urls.defaults import patterns, url

from .views import DeleteOrganizerView, DeleteWatcherView


urlpatterns = patterns('',
    url(r'^organizers/delete/(?P<pk>\d+)/$', DeleteOrganizerView.as_view(),
        name='delete_organizer'),
    url(r'^watchers/delete/(?P<pk>\d+)/$', DeleteWatcherView.as_view(),
        name='delete_watcher'),
)
