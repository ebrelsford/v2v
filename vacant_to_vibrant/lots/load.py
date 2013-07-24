"""
Utilities for loading lots, mostly from other models.

"""
import logging

import reversion

from phillydata.availableproperties.models import AvailableProperty
from phillydata.landuse.models import LandUseArea
from phillydata.licenses.models import License
from phillydata.parcels.models import Parcel
from phillydata.taxaccounts.models import TaxAccount
from phillydata.violations.models import Violation
from .models import Lot


logger = logging.getLogger(__name__)


def load_lots():
    load_lots_with_licenses()
    load_lots_with_violations()
    load_lots_available()
    load_lots_by_tax_account()


def load_lots_with_licenses():
    for license in License.objects.filter(lot=None):
        try:
            parcel = Parcel.objects.get_fuzzy(
                address=license.location.address,
                centroid=license.location.point
            )
        except (Parcel.MultipleObjectsReturned, Parcel.DoesNotExist):
            logger.warn('Could not find parcel for license: %s' % str(license))
            continue
        except Exception:
            logger.exception('Exception while finding Parcel for license: %s' %
                             str(license))
            continue

        with reversion.create_revision():
            lot = get_or_create_lot(
                parcel, license.location.address,
                centroid=license.location.point,
                zipcode=license.location.zip_code
            )
        if not lot.licenses.filter(pk=license.pk):
            lot.licenses.add(license)


def load_lots_with_violations():
    for violation in Violation.objects.filter(lot=None):
        try:
            parcel = Parcel.objects.get_fuzzy(
                address=violation.location.address,
                centroid=violation.location.point
            )
        except (Parcel.MultipleObjectsReturned, Parcel.DoesNotExist):
            logger.warn('Could not find parcel for violation: %s' %
                        str(violation))
            continue
        except Exception:
            logger.exception(('Exception while finding Parcel for violation: '
                              '%s') % str(violation))
            continue

        with reversion.create_revision():
            lot = get_or_create_lot(
                parcel, violation.location.address,
                centroid=violation.location.point,
                zipcode=violation.location.zip_code
            )
        if not lot.violations.filter(pk=violation.pk):
            lot.violations.add(violation)


def load_lots_available(added_after=None, force=False):
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
    if not force:
        properties = properties.filter(lot=None)
    for available_property in properties:
        address = available_property.address
        try:
            parcel = Parcel.objects.get_fuzzy(
                address=address,
                centroid=available_property.centroid,
                mapreg=available_property.mapreg
            )
        except Exception:
            logger.exception(('Exception while finding parcel for available '
                              'property: %s') % str(available_property))
            continue

        with reversion.create_revision():
            lot = get_or_create_lot(parcel, address,
                                    centroid=available_property.centroid)
            lot.available_property = available_property
            lot.save()


def load_lots_land_use_vacant(added_after=None, force=False):
    """
    Find Parcels and add Lots for LandUseAreas added after the given datetime.

    """
    areas = LandUseArea.objects.all()
    if not force:
        # don't try every LandUseArea unless we're asked to
        areas = LandUseArea.objects.filter(lot=None)
    if added_after:
        areas = areas.filter(added__gte=added_after)
    for area in areas:
        try:
            parcel = Parcel.objects.get_fuzzy(centroid=area.geometry.centroid)
        except (Parcel.MultipleObjectsReturned, Parcel.DoesNotExist):
            logger.warn('Could not find parcel for LandUseArea: %s' %
                        str(area))
        except Exception:
            logger.exception(('Unexpected exception finding parcel for '
                              'LandUseArea %s') % str(area))
            continue

        lot, created = Lot.objects.get_or_create(
            defaults=_get_lot_defaults(land_use_area=area, parcel=parcel),
            **_get_lot_kwargs(land_use_area=area, parcel=parcel)
        )
        lot.land_use_area = area
        lot.save()


def load_lots_by_tax_account(force=False):
    tax_accounts = TaxAccount.objects.filter(building_description='vacantLand')
    if not force:
        tax_accounts = tax_accounts.filter(lot=None)
    for tax_account in tax_accounts:
        address = tax_account.property_address
        try:
            parcel = Parcel.objects.get_fuzzy(address=address)
        except (Parcel.MultipleObjectsReturned, Parcel.DoesNotExist):
            logger.warn('Could not find parcel for tax account: %s' %
                        str(tax_account))
        except Exception:
            logger.exception(('Unexpected exception finding parcel for tax '
                              'account %s') % str(tax_account))
            continue

        lot = get_or_create_lot(parcel, address)
        lot.tax_account = tax_account
        lot.save()


def get_or_create_lot(parcel, address, polygon=None, centroid=None,
                      zipcode=None):
    defaults = _get_lot_defaults(address=address, parcel=parcel,
                                 centroid=centroid, polygon=polygon,
                                 zipcode=zipcode)
    kwargs = _get_lot_kwargs(address=address, parcel=parcel)

    # Try to update the lot (without a LotGroup), first
    existing_lot = Lot.objects.filter(lotgroup=None, **kwargs)
    if existing_lot.count() == 1:
        existing_lot.update(**defaults)
        return existing_lot[0]
    else:
        lot, created = Lot.objects.get_or_create(defaults=defaults, **kwargs)
        return lot


def _get_lot_kwargs(address=None, land_use_area=None, parcel=None):
    """Get a dictionary of kwargs for getting a distinct Lot."""
    kwargs = {}
    if address:
        kwargs['address_line1'] = address
    if parcel:
        if parcel.address:
            kwargs['address_line1'] = parcel.address
        else:
            kwargs['parcel'] = parcel
    if land_use_area:
        kwargs['land_use_area'] = land_use_area
    return kwargs


def _get_lot_defaults(address=None, centroid=None, land_use_area=None,
                      parcel=None, polygon=None, zipcode=None):
    """Get a dictionary of default values to set for a Lot."""
    if not polygon:
        if land_use_area and parcel:
            # If we have a land use area and a parcel, try to pick the shape of
            # the lot appropriately. If the land use area is significantly
            # smaller, use the land use area.
            parcel_area = parcel.geometry.transform(102729, clone=True).area
            if float(land_use_area.area) / parcel_area < .5:
                polygon = land_use_area.geometry
            else:
                polygon = parcel.geometry
        elif parcel:
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
