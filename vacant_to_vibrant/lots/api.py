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
        if 'centroid__within' in orm_filters and orm_filters['centroid__within'] == '':
            del orm_filters['centroid__within']

        if 'owner__name__icontains' in orm_filters and orm_filters['owner__name__icontains'] == '':
            del orm_filters['owner__name__icontains']

        if 'participant_types' in filters:
            participant_type_filters = Q()
            for participant_type in filters.getlist('participant_types', []):
                f = Q(**{
                    '%s__isnull' % participant_type: False,
                })
                participant_type_filters = participant_type_filters | f
            lots = Lot.objects.filter(participant_type_filters)
            orm_filters['pk__in'] = lots.values_list('pk', flat=True)

        if 'violations_count' in filters:
            try:
                violations_count = int(filters['violations_count'])
            except Exception:
                violations_count = 0
            if violations_count > 0:
                lots = Lot.objects.all().annotate(violations_count=Count('violations'))
                # TODO make this actually do something
                lots = lots.filter(violations_count=violations_count)

        try:
            impervious_area = int(filters['water_parcel__impervious_area__lt'])
            orm_filters['water_parcel__impervious_area__lt'] = impervious_area
        except Exception:
            pass

        boundary_filters = None
        for f in filters:
            if not f.startswith('boundary_'): continue
            layer = f.replace('boundary_', '').replace('_', ' ')
            boundaries = Boundary.objects.filter(
                layer__name__iexact=layer,
                label__in=filters.getlist(f),
            )
            for boundary in boundaries:
                boundary_filter = Q(centroid__within=boundary.geometry)
                if boundary_filters:
                    boundary_filters = boundary_filters | boundary_filter
                else:
                    boundary_filters = boundary_filter
        if boundary_filters:
            lots = Lot.objects.all().filter(boundary_filters)

            # TODO override apply_filters rather than use pk__in
            # like here:
                # http://stackoverflow.com/questions/10021749/django-tastypie-advanced-filtering-how-to-do-complex-lookups-with-q-objects
            orm_filters['pk__in'] = (orm_filters.get('pk__in', []) +
                                     list(lots.values_list('pk', flat=True)))

        # TODO fix weird hybrid of API/Django form-processing
        # -> Make the form widgets perform more like an API?
        form = FiltersForm(filters)
        form.is_valid()
        cleaned_data = form.cleaned_data

        if cleaned_data.get('parents_only', False):
            orm_filters['group__isnull'] = True

        for f in ('available_property', 'billing_account', 'tax_account',
                  'parcel', 'land_use_area', 'violations',):
            filter_name = 'has_%s' % f
            if filter_name in cleaned_data and cleaned_data[filter_name] is not None:
                orm_filters['%s__isnull' % f] = not cleaned_data[filter_name]

        for filter_name, value in cleaned_data.items():
            if filter_name in ('zoning_district__zoning_type__in',) and value:
                orm_filters[filter_name] = value

        return orm_filters

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
