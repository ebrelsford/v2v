"""
Utilities for loading parcel data.

"""
import os

from django.conf import settings
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon

from .models import Parcel


PARCEL_DATA_FILE = os.path.join(settings.DATA_ROOT,
                                'Parcels/PhiladelphiaParcels201201.shp')

ADDRESS_COMPONENTS = ('HOUSE', 'SUF', 'UNIT', 'STDIR', 'STNAM', 'STDES',
                      'STDESSUF')


def get_address(feature):
    # TODO massage a bit to match violation data
    return ' '.join([str(feature[k]) for k in ADDRESS_COMPONENTS if feature[k]])


def save_parcel(feature):
    geometry = feature.geom.transform(4326, clone=True).geos
    if isinstance(geometry, Polygon):
        geometry = MultiPolygon(geometry)

    parcel = Parcel(
        geometry=geometry,
        basereg=feature['BASEREG'],
        mapreg=feature['MAPREG'],
        stcod=feature['STCOD'],
        address=get_address(feature),
    )
    parcel.save()
    return parcel


def load_parcels(source=PARCEL_DATA_FILE):
    layer = DataSource(source)[0]
    for feature in layer:
        try:
            save_parcel(feature)
        except:
            print ('Could not save parcel for feature with OBJECTID=%s. '
                   'Skipping.') % feature['OBJECTID']
