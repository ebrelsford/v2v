from django.contrib.contenttypes.models import ContentType

from inplace.api.serializers import GeoJSONSerializer
from tastypie.contrib.gis.resources import ModelResource
from tastypie.resources import ALL

from organize.models import Organizer, Watcher
from .models import Lot


class GenericRelationFilterMixin(object):

    def add_generic_filter(self, orm_filters, generic_class):
        objs = generic_class.objects.filter(
            target_type=ContentType.objects.get_for_model(Lot),
        )
        pks = orm_filters.get('pk__in', [])
        orm_filters['pk__in'] = pks + list(set(objs.values_list('target_id',
                                                                flat=True)))
        return orm_filters


class LotResource(GenericRelationFilterMixin, ModelResource):

    def build_filters(self, filters={}):
        orm_filters = super(LotResource, self).build_filters(filters=filters)
        if 'centroid__within' in orm_filters and orm_filters['centroid__within'] == '':
            del orm_filters['centroid__within']
        participant_types = filters.getlist('participant_types', [])
        if 'organizers' in participant_types:
            orm_filters = self.add_generic_filter(orm_filters, Organizer)
        if 'watchers' in participant_types:
            orm_filters = self.add_generic_filter(orm_filters, Watcher)
        return orm_filters

    class Meta:
        queryset = Lot.objects.all()
        filtering = {
            'centroid': ALL,
            'polygon': ALL,
        }
        default_format = 'geojson'


class LotListResource(LotResource):
    """An abbreviated endpoint for getting lots of Lot data at once."""

    class Meta(LotResource.Meta):
        fields = ['id', 'centroid',]
        serializer = GeoJSONSerializer()
        max_limit = 100000
