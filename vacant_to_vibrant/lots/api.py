from django.db.models import Q

from inplace.api.serializers import GeoJSONSerializer
from tastypie.contrib.gis.resources import ModelResource
from tastypie.resources import ALL

from .models import Lot


class LotResource(ModelResource):

    def build_filters(self, filters={}):
        orm_filters = super(LotResource, self).build_filters(filters=filters)
        if 'centroid__within' in orm_filters and orm_filters['centroid__within'] == '':
            del orm_filters['centroid__within']

        participant_type_filters = Q()
        for participant_type in filters.getlist('participant_types', []):
            f = Q(**{
                '%s__isnull' % participant_type: False,
            })
            participant_type_filters = participant_type_filters | f
        orm_filters['pk__in'] = Lot.objects.filter(participant_type_filters).values_list('pk', flat=True)

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
