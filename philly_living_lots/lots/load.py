"""
Utilities for loading lots, mostly from other models.

"""
from .models import Lot
from phillydata.availableproperties.models import AvailableProperty
from phillydata.parcels.models import Parcel
from phillydata.violations.models import Violation


def load_lots():
    load_lots_with_violations()


def load_lots_with_violations():
    for violation in Violation.objects.all():
        parcel = find_parcel(violation.violation_location.point,
                             address=violation.violation_location.address)
        if not parcel:
            print 'No parcel found for violation:', violation
            continue

        # TODO centroid
        # TODO account for violations that don't agree with each other
        lot = get_or_create_lot(parcel, violation.violation_location.address,
                                centroid=None,
                                zipcode=violation.violation_location.zip_code)
        lot.violations.add(violation) # TODO check if it's already there?


def load_lots_available(added_after=None):
    properties = AvailableProperty.objects.all()
    if added_after:
        properties = properties.filter(added__gte=added_after)
    for available_property in properties:
        address = available_property.address
        parcel = find_parcel(available_property.centroid, address=address,
                             mapreg=available_property.mapreg)
        if not parcel:
            print 'No parcel found for available property:', available_property
            continue

        lot = get_or_create_lot(parcel, address,
                                centroid=available_property.centroid)
        lot.available_property = available_property
        lot.save()


def find_parcel(point, address=None, mapreg=None):
    # TODO couldn't this be in phillydata.parcels.* ?
    parcels = Parcel.objects.filter(
        geometry__contains=point,
    )
    if parcels.count() > 1:
        print 'Found too many parcels (%d) for point' % parcels.count(), point
        if address:
            print 'Trying to filter by address: "%s"' % address
            parcels = parcels.filter(address__iexact=address)
            if parcels.count() == 1:
                print '  ...success!'
                return parcels[0]
        if mapreg:
            print 'Trying to filter by mapreg: "%s"' % mapreg
            parcels = parcels.filter(mapreg=mapreg)
            if parcels.count() == 1:
                print '  ...success!'
                return parcels[0]

        print 'Still too many parcels:'
        for parcel in parcels:
            print '\tparcel:', parcel
    elif parcels.count() == 1:
        return parcels[0]
    else:
        print 'No parcels found for point', point


def get_or_create_lot(parcel, address, centroid=None, zipcode=None):
    lot, created = Lot.objects.get_or_create(
        address_line1=address,
        defaults={
            'parcel': parcel,
            'polygon': parcel.geometry,
            'centroid': centroid,
            'postal_code': zipcode,
            'city': 'Philadelphia',
            'state_province': 'PA',
            'country': 'USA',
        },
    )
    return lot

