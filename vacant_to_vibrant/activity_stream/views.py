from django.contrib.gis.feeds import GeoFeedMixin, GeoRSSFeed
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.views.generic import ListView

from actstream.models import Action


class PlaceActivityListView(ListView):
    model = Action
    paginate_by = 15
    template_name = 'activity/action_list.html'

    def get_queryset(self):
        qs = self.model.objects.public()
        filters = self.request.GET

        try:
            qs = self.model.objects.in_bbox(filters['bbox'].split(','))
        except Exception:
            pass
        return qs


class PlaceActivityFeed(Feed, GeoFeedMixin):
    feed_type = GeoRSSFeed
    subtitle = 'Recent activity'
    title = 'Site-wide activity stream'

    def items(self):
        return Action.objects.all().order_by('-timestamp')[:10]

    def item_extra_kwargs(self, item):
        return {'geometry' : self.item_geometry(item)}

    def item_geometry(self, item):
        return item.place

    def link(self):
        return reverse('activitystream_feed')
