from django.conf.urls.defaults import patterns, url

from .views import (PlacesWithViolationsView, PlacesWithViolationsMap,
                    LotsGeoJSON, LotsMap)


urlpatterns = patterns('',
    url(r'^violations/geojson/$', PlacesWithViolationsView.as_view()),
    url(r'^violations/map/$', PlacesWithViolationsMap.as_view()),

    url(r'^geojson/', LotsGeoJSON.as_view()),
    url(r'^', LotsMap.as_view()),
)
