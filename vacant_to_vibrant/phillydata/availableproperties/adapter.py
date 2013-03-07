import traceback

from django.contrib.gis.geos import Point
from django.core.exceptions import MultipleObjectsReturned
from django.utils.timezone import now

import reversion

from .api import AvailablePropertyReader
from .models import AvailableProperty


def find_available_properties():
    reader = AvailablePropertyReader()
    for available_property in reader:
        create_or_update(available_property)


def find_no_longer_available_properties(since):
    # check for AvailableProperty objects that were not seen this time
    no_longer_available = AvailableProperty.objects.filter(
        last_seen__lt=since
    )
    no_longer_available.update(status='no longer available')
    print 'Done updating %d no-longer-available Available Properties' % (
        no_longer_available.count(),
    )


@reversion.create_revision()
def create_or_update(available_property):
    try:
        field_dict = model_defaults(available_property)
        model, created = AvailableProperty.objects.get_or_create(
            defaults=field_dict,
            **model_get_kwargs(available_property)
        )
        if not created:
            field_dict['status'] = 'available'
            AvailableProperty.objects.filter(pk=model.pk).update(**field_dict)
            model = AvailableProperty.objects.get(pk=model.pk)
    except MultipleObjectsReturned:
        # TODO try to narrow it down?
        print ('Multiple objects found when searching for AvailableProperty '
               'objects with kwargs:', model_get_kwargs(available_property))
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
