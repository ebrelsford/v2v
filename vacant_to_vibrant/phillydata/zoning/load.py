"""
Utilities for loading zoning data.

"""
import os
import traceback

from django.conf import settings
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon

from .models import BaseDistrict, ZoningType


ZONING_DATA_FILE = os.path.join(settings.DATA_ROOT,
                                ('Zoning_BaseDistricts201208/'
                                 'PhiladelphiaZoning_BaseDistricts201208.shp'))


def _save_base_district(feature):
    geometry = feature.geom.transform(4326, clone=True).geos
    if isinstance(geometry, Polygon):
        geometry = MultiPolygon(geometry)

    base_district = BaseDistrict(
        geometry=geometry,
        zoning_type=ZoningType.objects.get_or_create(
            code=feature['CODE'],
            long_code=feature['LONG_CODE'],
            group=feature['ZONINGGROU'],
        )[0],
    )
    base_district.save()
    return base_district


def load_zoning_districts(source=ZONING_DATA_FILE):
    """
    Load zoning districts from the given shapefile.
    """
    layer = DataSource(source)[0]
    for feature in layer:
        try:
            _save_base_district(feature)
        except:
            print ('Could not save base district for feature with OBJECTID=%s.'
                   ' Skipping.') % feature['OBJECTID']
            traceback.print_exc()
