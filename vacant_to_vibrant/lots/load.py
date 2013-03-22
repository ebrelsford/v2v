"""
Utilities for loading lots, mostly from other models.

"""
from .models import Lot
from phillydata.availableproperties.models import AvailableProperty
from phillydata.landuse.models import LandUseArea
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
    """
    Find Parcels and add Lots for AvailableProperty added after the given
    datetime.

    Known issues: does not always find parcels associated, generally because
    the AvailableProperty data contains addresses that are ranges, eg,
    "1230 - 34 Burns St".

    """
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


def load_lots_land_use_vacant(added_after=None):
    """
    Find Parcels and add Lots for LandUseAreas added after the given datetime.

    """
    areas = LandUseArea.objects.all()
    if added_after:
        areas = areas.filter(added__gte=added_after)
    for area in areas:
        parcel = find_parcel(centroid=area.geometry.centroid)
        if not parcel:
            print 'No parcel found for LandUseArea:', area
            print '\tAdding lot with just LandUseArea'
        lot, created = Lot.objects.get_or_create(
            defaults=_get_lot_defaults(land_use_area=area, parcel=parcel),
            **_get_lot_kwargs(land_use_area=area, parcel=parcel)
        )

        lot.land_use_area = area
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


def get_or_create_lot(parcel, address, polygon=None, centroid=None,
                      zipcode=None):
    lot, created = Lot.objects.get_or_create(
        defaults=_get_lot_kwargs(address=address, parcel=parcel),
        **_get_lot_defaults(address=address, parcel=parcel, centroid=centroid,
                            polygon=polygon, zipcode=zipcode)
    )
    return lot


def _get_lot_kwargs(address=None, land_use_area=None, parcel=None):
    """Get a dictionary of kwargs for getting a distinct Lot."""
    if address:
        return { 'address_line1': address }
    if parcel:
        if parcel.address:
            return { 'address_line1': parcel.address }
        else:
            return { 'parcel': parcel }
    if land_use_area:
        return { 'land_use_area': land_use_area }


def _get_lot_defaults(address=None, centroid=None, land_use_area=None,
                      parcel=None, polygon=None, zipcode=None):
    """Get a dictionary of default values to set for a Lot."""
    if not polygon:
        if parcel:
            polygon = parcel.geometry
        elif land_use_area:
            polygon = land_use_area.geometry
        else:
            raise Exception('Lot requires a polygon')
    if not centroid:
        centroid = polygon.centroid
    if parcel and not address:
        address = parcel.address

    return {
        'parcel': parcel,
        'land_use_area': land_use_area,
        'address_line1': address,
        'polygon': polygon,
        'centroid': centroid,
        'city': 'Philadelphia',
        'state_province': 'PA',
        'country': 'USA',
        'postal_code': zipcode,
    }
