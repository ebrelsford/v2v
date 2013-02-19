from django.conf.urls.defaults import patterns, url

from .views import PlacesWithViolationsView, PlacesWithViolationsMap


urlpatterns = patterns('',
    url(r'^violations/geojson/$', PlacesWithViolationsView.as_view()),
    url(r'^violations/map/$', PlacesWithViolationsMap.as_view()),
)
