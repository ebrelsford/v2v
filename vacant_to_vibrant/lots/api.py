from django.db.models import Q, Count

from inplace.api.serializers import GeoJSONSerializer
from inplace.boundaries.models import Boundary
from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.resources import ALL, ALL_WITH_RELATIONS

from phillydata.owners.models import Owner
from .forms import FiltersForm
from .models import Lot, Use


class UseResource(ModelResource):

    class Meta:
        allowed_methods = ('get',)
        queryset = Use.objects.all()
        resource_name = 'use'
        fields = ('name',)
        filtering = {
            'name': ALL,
        }


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
    known_use = fields.ForeignKey(UseResource, 'known_use', null=True, blank=True)
    owner = fields.ForeignKey(OwnerResource, 'owner', null=True, blank=True)

    def build_filters(self, filters={}):
        orm_filters = super(LotResource, self).build_filters(filters=filters)

        # Remove empty bbox filter
        if 'centroid__within' in orm_filters and orm_filters['centroid__within'] == '':
            del orm_filters['centroid__within']

        # Remove empty owner name filter
        if 'owner__name__icontains' in orm_filters and orm_filters['owner__name__icontains'] == '':
            del orm_filters['owner__name__icontains']

        # Add participant types
        orm_filters['participant_types'] = filters.getlist('participant_types', [])

        # Add impervious area filters
        try:
            impervious_area = int(filters['water_parcel__impervious_area__lt'])
            orm_filters['water_parcel__impervious_area__lt'] = impervious_area
        except Exception:
            pass

        # Add boundary filters
        for f in filters:
            if not f.startswith('boundary_'): continue
            orm_filters[f] = filters.getlist(f)

        # TODO fix weird hybrid of API/Django form-processing
        # -> Make the form widgets perform more like an API?
        form = FiltersForm(filters)
        form.is_valid()
        cleaned_data = form.cleaned_data

        # Add violations count filter
        orm_filters['violations_count'] = cleaned_data.get('violations_count', 0)

        # Add parents only filter
        if cleaned_data.get('parents_only', False):
            orm_filters['group__isnull'] = True

        # Add has_* filters (checking for null on foreign key fields)
        for f in ('available_property', 'billing_account', 'tax_account',
                  'parcel', 'water_parcel', 'land_use_area', 'licenses',
                  'violations',):
            filter_name = 'has_%s' % f
            if filter_name in cleaned_data and cleaned_data[filter_name] is not None:
                orm_filters['%s__isnull' % f] = not cleaned_data[filter_name]

        for filter_name, value in cleaned_data.items():
            if filter_name in ('zoning_district__zoning_type__in',) and value:
                orm_filters[filter_name] = value

        return orm_filters

    def apply_filters(self, request, applicable_filters):

        #
        # Pop custom filters
        #
        cleaned_filters = applicable_filters.copy()

        # Pop boundary filters for once we have a queryset
        cleaned_boundary_filters = {}
        for f in applicable_filters:
            if not f.startswith('boundary_'): continue

            # Convert to layer name
            layer = f.replace('boundary_', '').replace('_', ' ')

            # Save for later
            cleaned_boundary_filters[layer] = cleaned_filters.pop(f)

        # Pop violations_count
        violations_count = cleaned_filters.pop('violations_count', 0)

        # Pop participant_types
        participant_types = cleaned_filters.pop('participant_types', [])

        #
        # Get queryset using the orm filters
        #
        qs = super(LotResource, self).apply_filters(request, cleaned_filters)

        #
        # Apply custom filters
        #

        # Apply boundary filters
        boundary_filters = None
        for layer, boundary_pks in cleaned_boundary_filters.items():
            boundaries = Boundary.objects.filter(
                layer__name__iexact=layer,
                label__in=boundary_pks,
            )

            for boundary in boundaries:
                boundary_filter = Q(centroid__within=boundary.geometry)
                if boundary_filters:
                    boundary_filters = boundary_filters | boundary_filter
                else:
                    boundary_filters = boundary_filter
        if boundary_filters: qs = qs.filter(boundary_filters)

        # Apply violations_count
        if violations_count > 0:
            qs = qs.annotate(violations_count=Count('violations'))
            qs = qs.filter(violations_count=violations_count)

        # Apply participant_types
        if participant_types:
            participant_type_filters = Q()
            for participant_type in participant_types:
                f = Q(**{
                    '%s__isnull' % participant_type: False,
                })
                participant_type_filters = participant_type_filters | f
            qs = qs.filter(participant_type_filters)

        return qs

    class Meta:
        allowed_methods = ('get',)
        fields = ('centroid', 'polygon', 'pk', 'owner', 'known_use',)
        queryset = Lot.objects.all()
        filtering = {
            'centroid': ALL,
            'known_use': ALL_WITH_RELATIONS,
            'owner': ALL_WITH_RELATIONS,
            'polygon': ALL,
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
        fields = ['id', 'centroid', 'owner', 'known_use',]

        # TODO or include?
        geojson_properties_exclude = ('owner', 'resource_uri', 'known_use',)
        max_limit = 100000
        serializer = GeoJSONSerializer()
