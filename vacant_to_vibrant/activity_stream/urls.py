from django.conf.urls.defaults import patterns, url

from activity_stream.views import PlaceActivityFeed, PlaceActivityListView


urlpatterns = patterns('',

    url(r'^feeds/all/$',
        PlaceActivityFeed(),
        name='activitystream_feed',
    ),

    url(r'^',
        PlaceActivityListView.as_view(),
        name='activitystream_activity_list'
    ),

)
