from datetime import datetime

import reversion

from .models import TaxAccount
from phillydata.opa.models import BillingAccount


@reversion.create_revision()
def create_or_update_tax_account(data, override={}):
    defaults = _defaults(data, override={})
    water_parcel, created = TaxAccount.objects.get_or_create(
        defaults=defaults, **_kwargs(data))
    if not created:
        TaxAccount.objects.filter(pk=water_parcel.pk).update(**defaults)
    return water_parcel


def _get_float(value, default=None):
    try:
        return float(value)
    except ValueError:
        return default


def _get_date(value, format='%Y%m%d', default=None):
    try:
        return datetime.strptime(value, format)
    except Exception:
        return None


def _defaults(data, override={}):
    try:
        billing_account = BillingAccount.objects.get(external_id=data['BRT NUM'])
    except Exception:
        billing_account = None
    defaults =  {
        'owner_name': data['LEGAL NAME'],
        'owner_name2': data['OWNER2 NAME'],
        'property_address': data['Property Address'],
        'property_city': data['CITY'],
        'property_state_province': data['ST'],
        'property_postal_code': data['ZIP5'],
        'building_description': data['Building Description'],
        'building_category': data['Building Category'],
        'billing_account': billing_account,
        'amount_delinquent': _get_float(data['CALC RCV TOTAL']),
        'years_delinquent': data['Count_of_Years'],
        'min_period': _get_date(data['Min_Period']),
        'max_period': _get_date(data['Max_Period']),
        'taxable_assessment': _get_float(data['Taxable Assessment']),
        'exempt_abate_assessment': _get_float(data['Exempt Abate Assessment']),
        'market_value': _get_float(data['Market Value']),
    }
    defaults.update(override)
    return defaults


def _kwargs(data):
    return {
        'brt_number': data['BRT NUM'],
    }
