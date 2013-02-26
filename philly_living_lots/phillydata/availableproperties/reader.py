import traceback

from django.contrib.gis.geos import Point
from django.utils.timezone import now

from arcgisrest.reader import ArcGISRestServerReader


class AvailablePropertyReader(ArcGISRestServerReader):
    """
    A class for iterating over available properties listed here:
        http://gis.phila.gov/ArcGIS/rest/services/RDA/PAPL_Web/MapServer/0/

    """
    def __init__(self):
        super(AvailablePropertyReader, self).__init__(
            'http://gis.phila.gov/ArcGIS/rest/services/RDA/PAPL_Web/MapServer/0/query?',
            'esriGeometryEnvelope',
            '-1.00006902217865,-1.00007303059101,2745294.56838398,300739.423707381'
        )

    def model_get_kwargs(self, feature):
        """
        Get AvailableProperty get() kwargs--useful for get_or_create()--for the
        given feature.

        """
        return {
            'asset_id': feature['attributes']['ASSET_ID'],
        }

    def model_defaults(self, feature):
        """
        Get AvailableProperty defaults--useful for get_or_create()--for the
        given feature.

        """
        try:
            return {
                'centroid': Point(feature['geometry']['x'],
                                  feature['geometry']['y']),
                'mapreg': feature['attributes']['MAPREG'],
                'address': feature['attributes']['REF_ADDRES'],
                'description': feature['attributes']['DESCR'],
                'agency': feature['attributes']['AGENCY'],
                'price': round(float(feature['attributes']['PRICE']), 2),
                'price_str': feature['attributes']['PRICE_STR'],
                'area': round(float(feature['attributes']['SQFEET']), 2),
                'status': 'new and available',
                'last_seen': now(),
            }
        except Exception:
            print 'Exception fetching Available Property model defaults!'
            print '    Feature:', feature
            traceback.print_stack()
            return None
