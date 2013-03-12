"""
Utilities for loading parcel data.

"""
import os
import traceback

from django.conf import settings
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon

from phillydata import utils
from .models import Parcel


PARCEL_DATA_FILE = os.path.join(settings.DATA_ROOT,
                                'Parcels/PhiladelphiaParcels201201.shp')


def make_address(feature):
    return utils.make_address(
        house_number=str(feature['HOUSE']),
        house_suffix=str(feature['SUF']),
        house_unit=str(feature['UNIT']),
        street_direction=str(feature['STDIR']),
        street_name=str(feature['STNAM']),
        street_description=str(feature['STDES']),
        street_description_suffix=str(feature['STDESSUF']),
    )


def save_parcel(feature):
    geometry = feature.geom.transform(4326, clone=True).geos
    if isinstance(geometry, Polygon):
        geometry = MultiPolygon(geometry)

    address = make_address(feature)
    if address is '0':
        address = None
    parcel = Parcel(
        geometry=geometry,
        basereg=feature['BASEREG'],
        mapreg=feature['MAPREG'],
        stcod=feature['STCOD'],
        address=address,
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
            traceback.print_exc()
