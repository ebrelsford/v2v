import logging

from django.contrib.gis.geos import Point
from django.core.exceptions import MultipleObjectsReturned
from django.utils.timezone import now

import reversion

from ..utils import fix_address
from .api import AvailablePropertyReader
from .models import AvailableProperty


logger = logging.getLogger(__name__)


def find_available_properties():
    reader = AvailablePropertyReader()
    for available_property in reader:
        try:
            create_or_update(available_property)
        except Exception:
            logger.exception(('Unexpected exception while adding '
                              'AvailableProperty "%s"') % available_property)


def find_no_longer_available_properties(since):
    """
    Check for AvailableProperty objects that were not seen the last time we
    looked.
    """
    logger.info('Looking for no-longer-available AvailableProperty objects.')

    no_longer_available = AvailableProperty.objects.filter(
        last_seen__lt=since
    ).update(status='no longer available')

    logger.info(('Found and updated %d no-longer-available AvailableProperties '
                 'objects') % no_longer_available)


@reversion.create_revision()
def create_or_update(available_property):
    try:
        defaults = model_defaults(available_property)
        kwargs = model_get_kwargs(available_property)
        model, created = AvailableProperty.objects.get_or_create(
            defaults=defaults,
            **kwargs
        )
        if not created:
            defaults['status'] = 'available'
            AvailableProperty.objects.filter(pk=model.pk).update(**defaults)
            model = AvailableProperty.objects.get(pk=model.pk)
    except MultipleObjectsReturned:
        logger.exception(('Multiple objects found when searching for '
                          'AvailableProperty with kwargs: %s') % str(kwargs))
    return model


def model_get_kwargs(feature):
    """
    Get AvailableProperty get() kwargs--useful for get_or_create()--for the
    given feature.

    """
    return {
        'asset_id': feature['attributes']['ASSET_ID'],
    }


def model_defaults(feature):
    """
    Get AvailableProperty defaults--useful for get_or_create()--for the
    given feature.

    """
    try:
        return {
            'centroid': Point(feature['geometry']['x'],
                              feature['geometry']['y']),
            'mapreg': feature['attributes']['MAPREG'],
            'address': fix_address(feature['attributes']['REF_ADDRES']),
            'description': feature['attributes']['DESCR'],
            'agency': feature['attributes']['AGENCY'],
            'price': round(float(feature['attributes']['PRICE']), 2),
            'price_str': feature['attributes']['PRICE_STR'],
            'area': round(float(feature['attributes']['SQFEET']), 2),
            'status': 'new and available',
            'last_seen': now(),
        }
    except Exception:
        logger.exception(('Exception fetching Available Property model '
                          'defaults for feature %s') % feature)
        return None
