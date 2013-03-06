import geojson

from django.contrib.gis.geos.point import GEOSGeometry
from tastypie.serializers import Serializer


class GeoJSONSerializer(Serializer):
    formats = ['geojson',] # 'json']
    content_types = {
        'geojson': 'application/json',
        # TODO theoretically possible to use json, too, but impossibe to get
        #  geojson if this is included
        #'json': 'application/json',
    }

    def to_geojson(self, data, options={}):
        data = self.to_simple(data, options)

        if 'objects' in data:
            print len(data['objects'])
            return geojson.dumps(self._get_feature_collection(data['objects']))
        return data

    def _get_feature_collection(self, places):
        return geojson.FeatureCollection(
            features=[self._get_feature(place) for place in places],
        )

    def _get_feature(self, place):
        centroid = GEOSGeometry(place['centroid'])
        return geojson.Feature(
            place['id'],
            geometry=geojson.Point(
                coordinates=(centroid.x, centroid.y),
            ),
            properties=place,
        )
