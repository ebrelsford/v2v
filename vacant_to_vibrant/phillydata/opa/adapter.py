"""
Turns data from the OPA API into the relevant models.

Kind of a proxy/adapter for OPA data.

"""
from datetime import datetime
import logging

import reversion

from .api import get_account_data, get_address_data
from .models import AccountOwner, BillingAccount
from phillydata.owners.models import Owner
from vacant_to_vibrant.utils import html_unescape


logger = logging.getLogger(__name__)

SALE_DATE_FORMAT = '%m/%d/%Y'

def billing_account_kwargs(data):
    return {
        'external_id': data['account_information']['account_number'],
    }


def billing_account_defaults(data, defaults={}):
    acct_det = data['account_details']
    defaults.update(get_address(data))
    defaults.update({
        'sale_date': datetime.strptime(acct_det['sale_date'], SALE_DATE_FORMAT),
        'land_area': float(acct_det['land_area'].split()[0]),

        # TODO NB: if 0, could indicate vacancy
        'improvement_area': float(acct_det['improvement_area'].split()[0]),

        # TODO NB: if starts with 'VAC LAND', could indicate vacancy
        'improvement_description': acct_det['improvement_desc'],

        # TODO NB: if 0, could indicate publicly owned?
        'assessment': str(acct_det['assessment']).translate(None, '$,'),
    })
    return defaults


def get_address(data):
    addr = data['account_information']['mailing_address']
    address_details = {
        'property_address': data['account_information']['address'],
        'mailing_name': addr['street'][0],
        'mailing_address': addr['street'][1],
        'mailing_city': addr['city'],
        'mailing_state_province': addr['state'],
        'mailing_postal_code': addr['zip'],
    }
    # html_unescape everything
    return dict([(k, html_unescape(v)) for k, v in address_details.items()])


@reversion.create_revision()
def get_or_create_account_owner(data):
    account = data['account_information']

    # sorting owner names to keep internally consistent
    owner_name = ', '.join(sorted(account['owners']))
    owner_name = html_unescape(owner_name)

    account_owner, created = AccountOwner.objects.get_or_create(
        name=owner_name,
        defaults={ 'owner': Owner.objects.get_or_create(owner_name)[0], }
    )
    return account_owner


@reversion.create_revision()
def get_or_create_billing_account(data, account_owner):
    defaults = billing_account_defaults(data,
                                        {'account_owner': account_owner,})
    billing_account, created = BillingAccount.objects.get_or_create(
        defaults=defaults, **billing_account_kwargs(data))
    if not created:
        BillingAccount.objects.filter(pk=billing_account.pk).update(**defaults)
    return billing_account


def find_opa_details(address, brt_account=None):
    """Get or create a BillingAccount for the given address."""
    logger.debug('Getting OPA data for address "%s"' % address)

    # Attempt to get owner by address
    data = get_address_data(address)

    # Attempt to get owner by BRT number
    if brt_account and not data:
        logger.debug('Getting OPA data for account "%s"' % brt_account)
        data = get_account_data(brt_account)

    if not data:
        raise Exception('Could not find OPA details for "%s"' % address)

    account_owner = get_or_create_account_owner(data)
    return get_or_create_billing_account(data, account_owner)
