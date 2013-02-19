from tastypie.constants import ALL
from tastypie.resources import ModelResource

from places.api.serializers import GeoJSONSerializer
from pops.models import Building

# more complex filters: http://stackoverflow.com/questions/10021749/django-tastypie-advanced-filtering-how-to-do-complex-lookups-with-q-objects

# TODO for each subclass of Place
class BuildingResource(ModelResource):
    class Meta:
        default_format = 'geojson'
        filtering = {
            # TODO for all (public?) fields in model
            'address_line1': ALL,
        }
        queryset = Building.objects.all()
        serializer = GeoJSONSerializer()
