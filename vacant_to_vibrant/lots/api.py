from inspect import getmembers

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
            'owner_type': ALL_WITH_RELATIONS,
        }


class LotResource(ModelResource):
    known_use = fields.ForeignKey(UseResource, 'known_use', null=True, blank=True)

    def build_filters(self, filters={}):
        orm_filters_filters = filters.copy()

        # Remove the bits we won't actually be filtering on
        if 'centroid' in orm_filters_filters:
            del orm_filters_filters['centroid']
        if 'zoom' in orm_filters_filters:
            del orm_filters_filters['zoom']

        orm_filters = super(LotResource, self).build_filters(filters=orm_filters_filters)

        # Remove empty bbox filter
        if 'centroid__within' in orm_filters and orm_filters['centroid__within'] == '':
            del orm_filters['centroid__within']

        # Remove empty owner name filter
        if 'owner__name__icontains' in orm_filters and orm_filters['owner__name__icontains'] == '':
            del orm_filters['owner__name__icontains']

        orm_filters['owner__owner_type__in'] = filters.getlist('owner__owner_type__in', [])

        orm_filters['known_use_existence'] = filters.getlist('known_use_existence', [])

        # Add participant types
        orm_filters['participant_types'] = filters.getlist('participant_types', [])

        # Add available property statuses
        orm_filters['available_property__status__in'] = filters.getlist('available_property__status__in', [])

        # Add area gt
        orm_filters['polygon_area__gt'] = filters.get('polygon_area__gt', 0)
        orm_filters['polygon_area__lt'] = filters.get('polygon_area__lt', 0)

        # Add width gt
        orm_filters['polygon_width__gt'] = filters.get('polygon_width__gt', 0)
        orm_filters['polygon_width__lt'] = filters.get('polygon_width__lt', 0)

        # Add impervious area filters
        try:
            impervious_area = int(filters['water_parcel__impervious_area__lt'])
            orm_filters['water_parcel__impervious_area__lt'] = impervious_area
        except Exception:
            pass

        # Add boundary filters
        for f in filters:
            if not f.startswith('boundary_'): continue

            # Skip if we've already seen it
            if f in orm_filters: continue

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
        cleaned_filters = applicable_filters.copy()
        custom_filters = self._pop_custom_filters(cleaned_filters)
        qs = super(LotResource, self).apply_filters(request, cleaned_filters)
        return self._apply_custom_filters(qs, custom_filters)

    # Custom filters
    def _pop_custom_filters(self, filters):
        """
        Pop the custom filters from the given filters--modifying the given
        filters dict--and return a dict of custom filters.
        """
        custom_filters = {}
        for attr, value in getmembers(self):
            if not attr.startswith('pop_custom_filter_'): continue
            filter_name = attr.replace('pop_custom_filter_', '')
            custom_filters[filter_name] = getattr(self, attr)(filters)
        return custom_filters

    def _apply_custom_filters(self, qs, custom_filters):
        """Apply the custom filters that were popped."""
        for attr, value in getmembers(self):
            if not attr.startswith('apply_custom_filter_'): continue
            filter_name = attr.replace('apply_custom_filter_', '')
            qs = getattr(self, attr)(qs, custom_filters[filter_name])
        return qs

    def pop_custom_filter_boundary(self, filters):
        # Hold on to all filters while popping
        filters_copy = filters.copy()

        # Pop boundary filters for once we have a queryset
        boundary = {}
        for f in filters_copy:
            if not f.startswith('boundary_'): continue

            # Convert to layer name
            layer = f.replace('boundary_', '').replace('_', ' ')

            # Save for later
            boundary[layer] = filters.pop(f)
        return boundary

    def pop_custom_filter_available_property__status__in(self, filters):
        return filters.pop('available_property__status__in', [])

    def pop_custom_filter_violations_count(self, filters):
        return filters.pop('violations_count', 0)

    def pop_custom_filter_participant_types(self, filters):
        return filters.pop('participant_types', [])

    def pop_custom_filter_polygon_area__gt(self, filters):
        try:
            return int(filters.pop('polygon_area__gt'))
        except Exception:
            return 0

    def pop_custom_filter_polygon_area__lt(self, filters):
        try:
            return int(filters.pop('polygon_area__lt'))
        except Exception:
            return 0

    def pop_custom_filter_polygon_width__gt(self, filters):
        try:
            return int(filters.pop('polygon_width__gt'))
        except Exception:
            return 0

    def pop_custom_filter_polygon_width__lt(self, filters):
        try:
            return int(filters.pop('polygon_width__lt'))
        except Exception:
            return 0

    def pop_custom_filter_known_use_existence(self, filters):
        try:
            return filters.pop('known_use_existence', [])
        except Exception:
            return 0

    def pop_custom_filter_owner__owner_type__in(self, filters):
        return filters.pop('owner__owner_type__in', [])

    def apply_custom_filter_boundary(self, qs, value):
        boundary_filters = None
        for layer, boundary_pks in value.items():
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
        return qs

    def apply_custom_filter_available_property__status__in(self, qs, value):
        """
        If there are statuses, ensure those lots that are associated with
        available property have one of those statuses.
        """
        if value:
            qs = qs.filter(
                Q(available_property__isnull=True) |
                Q(available_property__status__in=value)
            )
        return qs

    def apply_custom_filter_violations_count(self, qs, value):
        if value > 0:
            qs = qs.annotate(violations_count=Count('violations'))
            qs = qs.filter(violations_count=value)
        return qs

    def apply_custom_filter_participant_types(self, qs, value):
        if value:
            participant_type_filters = Q()
            for participant_type in value:
                f = Q(**{
                    '%s__isnull' % participant_type: False,
                })
                participant_type_filters = participant_type_filters | f
            qs = qs.filter(participant_type_filters)
        return qs

    def apply_custom_filter_polygon_area__gt(self, qs, value):
        if value > 0:
            qs = qs.filter(
                polygon_area__isnull=False,
                polygon_area__gt=value,
            )
        return qs

    def apply_custom_filter_polygon_area__lt(self, qs, value):
        if value > 0:
            qs = qs.filter(
                polygon_area__isnull=False,
                polygon_area__lt=value,
            )
        return qs

    def apply_custom_filter_polygon_width__gt(self, qs, value):
        if value > 0:
            qs = qs.filter(
                polygon_width__isnull=False,
                polygon_width__gt=value,
            )
        return qs

    def apply_custom_filter_polygon_width__lt(self, qs, value):
        if value > 0:
            qs = qs.filter(
                polygon_width__isnull=False,
                polygon_width__lt=value,
            )
        return qs

    def apply_custom_filter_known_use_existence(self, qs, value):
        # Only change the queryset if exactly one type of existence is
        # selected
        if len(value) == 1:
            qs = qs.filter(
                known_use__isnull='not in use' in value,
            )
        return qs

    def apply_custom_filter_owner__owner_type__in(self, qs, value):
        # Make owner__owner_type__in look the way tastypie wants it to
        if 'mixed' in value:
            return qs.filter(
                Q(owner__owner_type__in=value) | Q(owner__isnull=True)
            )
        else:
            return qs.filter(
                owner__owner_type__in=value,
            )

    class Meta:
        allowed_methods = ('get',)
        fields = ('centroid', 'polygon', 'pk', 'known_use',
                  'known_use_certainty',)
        queryset = Lot.objects.all()
        filtering = {
            'centroid': ALL,
            'known_use': ALL_WITH_RELATIONS,
            'known_use_certainty': ALL_WITH_RELATIONS,
            'polygon': ALL,
        }


class VisibleLotResource(LotResource):
    """
    A LotResource that will only return lots that should be publicly visible.
    """

    class Meta(LotResource.Meta):
        queryset = Lot.visible.all()


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
