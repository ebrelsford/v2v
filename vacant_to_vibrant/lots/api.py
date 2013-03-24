from django.contrib.contenttypes.models import ContentType

from inplace.api.serializers import GeoJSONSerializer
from tastypie.contrib.gis.resources import ModelResource
from tastypie.resources import ALL

from organize.models import Organizer, Watcher
from .models import Lot


class GenericRelationFilterMixin(object):

    def add_generic_filter(self, filters, orm_filters, filter_name,
                           generic_class):
        if filters.get(filter_name, None) != 'True':
            return orm_filters
        objs = generic_class.objects.filter(
            target_type=ContentType.objects.get_for_model(Lot),
        )
        if not orm_filters.get('pk__in', None):
            orm_filters['pk__in'] = []
        orm_filters['pk__in'] += objs.values_list('target_id', flat=True)
        return orm_filters


class LotResource(GenericRelationFilterMixin, ModelResource):

    def build_filters(self, filters={}):
        orm_filters = super(LotResource, self).build_filters(filters=filters)
        orm_filters = self.add_generic_filter(filters, orm_filters,
                                              'organizers', Organizer)
        orm_filters = self.add_generic_filter(filters, orm_filters,
                                              'watchers', Watcher)
        return orm_filters

    class Meta:
        queryset = Lot.objects.all()
        filtering = {
            'polygon': ALL,
        }
        default_format = 'geojson'


class LotListResource(LotResource):
    """An abbreviated endpoint for getting lots of Lot data at once."""

    class Meta(LotResource.Meta):
        fields = ['id', 'centroid',]
        serializer = GeoJSONSerializer()
