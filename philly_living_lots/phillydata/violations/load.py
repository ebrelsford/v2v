from django.contrib.gis.geos import Point

from .models import Violation, ViolationLocation, ViolationType
from .reader import LIViolationReader


"""
codes worth looking at (from Stacey at L&I):
    CP-802
    PM-102.4/1
    PM-302.2/4
    PM-306.0/2
    PM-306.0/91
    PM-307.1/21
"""


def load_violations(code, year=2013):
    reader = LIViolationReader()
    for violation in reader.get(code, year):
        saved_violation = save_violation(violation)
        print saved_violation


def get_location(violation):
    location = violation['locations']
    (lon, lat) = LIViolationReader.get_lon_lat(location)
    address = LIViolationReader.make_address(location)

    # TODO only if point will be valid
    violation_location, created = ViolationLocation.objects.get_or_create(
        address=address,
        external_id=location['location_id'],
        point=Point(lon, lat),
        zip_code=location['zip'],
    )
    return violation_location


def get_violation_type(violation):
    # get type
    violation_type, created = ViolationType.objects.get_or_create(
        code=violation['violation_code'],
        li_description=violation['violation_code_description'],
    )
    return violation_type


def save_violation(violation):
    violation_location = get_location(violation)
    violation_type = get_violation_type(violation)

    saved_violation, created = Violation.objects.get_or_create(
        external_id=violation['violation_details_id'],
        violation_datetime=LIViolationReader.get_datetime(violation.get('violation_datetime', None)),
        violation_location=violation_location,
        violation_type=violation_type,
    )

    return saved_violation
