"""
Maps data from the Water Department API to this package's models.

"""
import logging

from .api import get_point_data
from .models import WaterAccount, WaterParcel


logger = logging.getLogger(__name__)


def find_water_dept_details(lon, lat):
    """Get or create WaterParcel, WaterAccount for the given lon and lat."""
    logger.debug('Getting Water Department data for %f, %f' % (lon, lat))
    data = get_point_data(lon, lat)
    if not data:
        raise Exception('Could not find Water Department data for %f, %f' %
                        (lon, lat))
    print 'Found data', data

    water_parcel = _get_or_create_water_parcel(data)
    _get_or_create_water_accounts(data, water_parcel)
    return water_parcel


def _get_or_create_water_parcel(data):
    defaults = _water_parcel_defaults(data)
    water_parcel, created = WaterParcel.objects.get_or_create(
        defaults=defaults, **_water_parcel_kwargs(data))
    if not created:
        WaterParcel.objects.filter(pk=water_parcel.pk).update(**defaults)
    return water_parcel


def _get_or_create_water_accounts(data, water_parcel):
    water_accounts = []
    for account in data['Accounts']:
        defaults = _water_account_defaults(
            account,
            defaults={ 'water_parcel': water_parcel }
        )
        water_account, created = WaterAccount.objects.get_or_create(
            defaults=defaults, **_water_account_kwargs(account))
        if not created:
            WaterAccount.objects.filter(pk=water_account.pk).update(**defaults)
        water_accounts.append(water_account)
    return water_accounts


def _water_parcel_kwargs(data):
    parcel = data['Parcel']
    return {
        'parcel_id': parcel['ParcelID'],
    }


def _water_parcel_defaults(data):
    parcel = data['Parcel']
    return {
        'brt_account': parcel['BRTAcct'],
        'ten_code': parcel['TenCode'],
        'owner1': parcel['Owner1'],
        'owner2': parcel['Owner2'],
        'address': parcel['Address'],
        'gross_area': parcel['GrossArea'],
        'impervious_area': parcel['ImpervArea'],
    }


def _water_account_kwargs(account_data):
    return {
        'account_id': account_data['WaterAccount'],
    }


def _water_account_defaults(account_data, defaults={}):
    defaults.update({
        'account_number': account_data['AccountNumber'],
        'customer_id': account_data['CustomerID'],
        'customer_name': account_data['CustomerName'],
        'inst_id': account_data['InstID'],
        'account_status': account_data['AcctStatus'],
        'account_status_abbreviation': account_data['AccountStatusAbbrev'],
        'meter_size': account_data['MeterSize'],
        'meter_size_abbreviation': account_data['MeterSizeAbbrev'],
        'service_type': account_data['ServiceType'],
        'service_type_label': account_data['ServiceTypeLabel'],
        'stormwater_status': account_data['StormwaterStatus'],
    })
    return defaults
