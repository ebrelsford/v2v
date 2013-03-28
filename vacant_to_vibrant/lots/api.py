from django.db.models import Q

from inplace.api.serializers import GeoJSONSerializer
from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.resources import ALL, ALL_WITH_RELATIONS

from phillydata.owners.models import Owner
from .models import Lot


class OwnerResource(ModelResource):

    class Meta:
        allowed_methods = ('get',)
        queryset = Owner.objects.all()
        resource_name = 'owner'
        fields = ('name', 'owner_type',)
        filtering = {
            'name': ALL,
            'owner_type': ALL,
        }


class LotResource(ModelResource):
    owner = fields.ForeignKey(OwnerResource, 'owner', null=True, blank=True)

    def build_filters(self, filters={}):
        orm_filters = super(LotResource, self).build_filters(filters=filters)
        if 'centroid__within' in orm_filters and orm_filters['centroid__within'] == '':
            del orm_filters['centroid__within']

        if 'participant_types' in filters:
            participant_type_filters = Q()
            for participant_type in filters.getlist('participant_types', []):
                f = Q(**{
                    '%s__isnull' % participant_type: False,
                })
                participant_type_filters = participant_type_filters | f
            lots = Lot.objects.filter(participant_type_filters)
            orm_filters['pk__in'] = lots.values_list('pk', flat=True)

        return orm_filters

    class Meta:
        allowed_methods = ('get',)
        fields = ('centroid', 'polygon', 'pk', 'owner',)
        queryset = Lot.objects.all()
        filtering = {
            'centroid': ALL,
            'polygon': ALL,
            'owner': ALL_WITH_RELATIONS,
        }


class LotListResource(LotResource):
    """An abbreviated endpoint for getting lots of Lot data at once."""

    def dehydrate(self, bundle):
        for exclude in self._meta.geojson_properties_exclude:
            del bundle.data[exclude]
        return bundle

    class Meta(LotResource.Meta):
        allowed_methods = ('get',)
        default_format = 'geojson'
        fields = ['id', 'centroid', 'owner',]
        geojson_properties_exclude = ('owner', 'resource_uri',) # TODO or include?
        max_limit = 100000
        serializer = GeoJSONSerializer()
