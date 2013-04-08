import geojson

from inplace.boundaries.models import Layer
from inplace.views import GeoJSONListView

from phillydata.parcels.models import Parcel


class FindParcelView(GeoJSONListView):

    def get_feature(self, parcel):
        try:
            zipcodes = Layer.objects.get(name='zipcodes')
            zipcode = zipcodes.boundary_set.get(
                geometry__contains=parcel.geometry,
            ).label
        except Exception:
            zipcode = ''

        return geojson.Feature(
            parcel.id,
            geometry=geojson.MultiPolygon(
                coordinates=parcel.geometry.coords,
            ),
            properties={
                'address': parcel.address,
                'lot_count': parcel.lot_set.count(),
                'zipcode': zipcode,
            },
        )

    def get_queryset(self):
        parcels = Parcel.objects.all()

        try:
            return parcels.filter(pk=self.request.GET['pk'])
        except Exception:
            try:
                return parcels.filter(
                    address__icontains=self.request.GET['address']
                )
            except Exception:
                pass

        return None
