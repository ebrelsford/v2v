import geojson

from django.views.generic import TemplateView

from phillydata.parcels.models import Parcel
from phillydata.violations.models import Violation, ViolationLocation
from places.views import GeoJSONListView
from .models import Lot


class PlacesWithViolationsView(GeoJSONListView):

    def get_feature(self, parcel):
        violation = Violation.objects.filter(violation_location__point__within=parcel.geometry)[0]

        return geojson.Feature(
            parcel.id,
            geometry=geojson.MultiPolygon(
                coordinates=parcel.geometry.coords,
            ),
            properties={
                'type': violation.violation_type.code,
                'description': violation.violation_type.li_description,
            },
        )

    def get_queryset(self):
        parcels = [Parcel.objects.filter(geometry__contains_properly=loc.point)[0] for loc in ViolationLocation.objects.all()]
        pks = [p.pk for p in parcels]
        return Parcel.objects.filter(pk__in=pks)


class PlacesWithViolationsMap(TemplateView):
    template_name = 'lots/places_with_violations.html'

    #def get_context_data(self, **kwargs):
        #context = super(TemplateView, self).get_context_data(**kwargs)
        #return context


class LotsGeoJSON(GeoJSONListView):

    def get_feature(self, lot):
        try:
            owner_name = lot.owner.name
        except Exception:
            owner_name = 'unknown'

        return geojson.Feature(
            lot.pk,
            geometry=geojson.MultiPolygon(
                coordinates=lot.polygon.coords,
            ),
            properties={
                'is_available': lot.available_property is not None,
                'owner': owner_name,
            },
        )

    def get_queryset(self):
        return Lot.objects.all().select_related('owner', 'available_property')


class LotsMap(TemplateView):
    template_name = 'lots/map.html'
