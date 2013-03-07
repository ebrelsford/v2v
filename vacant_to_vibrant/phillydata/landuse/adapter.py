import logging

from django.contrib.gis.geos import MultiPolygon, Polygon
from django.core.exceptions import MultipleObjectsReturned

from .api import LandUseReader
from .models import LandUseArea


logger = logging.getLogger(__name__)


def find_land_use_areas():
    reader = LandUseReader()
    for land_use_area in reader:
        create_or_update(land_use_area)


def create_or_update(land_use_area):
    try:
        field_dict = model_defaults(land_use_area)
        model, created = LandUseArea.objects.get_or_create(
            defaults=field_dict,
            **model_get_kwargs(land_use_area)
        )
        if not created:
            LandUseArea.objects.filter(pk=model.pk).update(**field_dict)
            model = LandUseArea.objects.get(pk=model.pk)
    except MultipleObjectsReturned:
        # TODO try to narrow it down?
        print ('Multiple objects found when searching for LandUseArea objects '
               'with kwargs:', model_get_kwargs(land_use_area))
    return model


def model_get_kwargs(feature):
    """
    Get LandUseArea get() kwargs--useful for get_or_create()--for the feature.

    """
    return {
        'object_id': feature['attributes']['OBJECTID'],
    }

def model_defaults(feature):
    """
    Get LandUseArea defaults--useful for get_or_create()--for the feature.

    """
    try:
        polygons = [Polygon(p) for p in feature['geometry']['rings']]
        return {
            'geometry': MultiPolygon(*polygons),
            'category': feature['attributes']['C_DIG1DESC'],
            'subcategory': feature['attributes']['C_DIG2DESC'],
            'description': feature['attributes']['C_DIG3DESC'],
            'vacant_building': feature['attributes']['VACBLDG'],
            'area': round(float(feature['attributes']['SHAPE_Area']), 2),
        }
    except Exception:
        logger.exception('Exception fetching LandUseArea model defaults! '
                         'OBJECTID: %s' % feature['attributes']['OBJECTID'])
        return None
