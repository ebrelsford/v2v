"""
Utilities for loading lots, mostly from other models.

"""
from .models import Lot
from phillydata.availableproperties.models import AvailableProperty
from phillydata.parcels.utils import find_parcel
from phillydata.taxaccounts.models import TaxAccount
from phillydata.violations.models import Violation


def load_lots():
    load_lots_with_violations()
    load_lots_available()
    load_lots_by_tax_account()


def load_lots_with_violations():
    for violation in Violation.objects.filter(lot=None):
        parcel = find_parcel(centroid=violation.violation_location.point,
                             address=violation.violation_location.address)
        if not parcel:
            print 'No parcel found for violation:', violation
            continue

        # TODO account for violations that don't agree with each other
        lot = get_or_create_lot(parcel, violation.violation_location.address,
                                centroid=violation.violation_location.point,
                                zipcode=violation.violation_location.zip_code)
        if not lot.violations.filter(pk=violation.pk):
            lot.violations.add(violation)


def load_lots_available(added_after=None):
    properties = AvailableProperty.objects.all()
    if added_after:
        properties = properties.filter(added__gte=added_after)
    for available_property in properties:
        address = available_property.address
        parcel = find_parcel(centroid=available_property.centroid,
                             address=address, mapreg=available_property.mapreg)
        if not parcel:
            print 'No parcel found for available property:', available_property
            continue

        lot = get_or_create_lot(parcel, address,
                                centroid=available_property.centroid)
        lot.available_property = available_property
        lot.save()


def load_lots_by_tax_account():
    tax_accounts = TaxAccount.objects.filter(building_description='vacantLand')
    for tax_account in tax_accounts:
        address = tax_account.property_address
        parcel = find_parcel(address=address)

        if not parcel:
            print 'No parcel found for tax account:', tax_account
            continue

        lot = get_or_create_lot(parcel, address)
        lot.tax_account = tax_account
        lot.save()


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
