from django.contrib.gis.geos import Point

from .api import LIReader
from .models import Location


def get_location(li_record):
    """Get the location from the given L&I record"""
    location = li_record['locations']
    (lon, lat) = LIReader.get_lon_lat(location)
    address = LIReader.make_address(location)

    # TODO only if point will be valid
    li_location, created = Location.objects.get_or_create(
        address=address,
        external_id=location['location_id'],
        point=Point(lon, lat),
        zip_code=location['zip'],
    )
    return li_location
