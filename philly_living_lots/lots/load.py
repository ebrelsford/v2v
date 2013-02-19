"""
Utilities for loading lots, mostly from other models.

"""

from datetime import datetime

from .models import Lot
from phillydata.opa.api import get_address_data
from phillydata.owners.models import BillingAccount, Owner
from phillydata.parcels.models import Parcel
from phillydata.violations.models import Violation
from utils import html_unescape

SALE_DATE_FORMAT = '%m/%d/%Y'


def load_lots():
    load_lots_with_violations()


def load_lots_with_violations():
    for violation in Violation.objects.all():
        parcel = find_parcel(violation)
        if not parcel:
            print 'No parcel found for violation:', violation
            continue

        lot, created = Lot.objects.get_or_create(
            address_line1=violation.violation_location.address,

            # TODO centroid
            # TODO account for violations that don't agree with each other
            defaults={
                'parcel': parcel,
                'polygon': parcel.geometry,

                'postal_code': violation.violation_location.zip_code,
                'city': 'Philadelphia',
                'state_province': 'PA',
                'country': 'USA',
            },
        )
        lot.violations.add(violation) # TODO check if it's already there?


def find_parcel(violation):
    parcels = Parcel.objects.filter(
        geometry__contains=violation.violation_location.point,
    )
    if parcels.count() != 1:
        print 'Found an unexpected number of parcels (%d) for violation' % parcels.count(), violation
        # TODO try to find one with matching address
        for parcel in parcels:
            print parcel
    return parcels[0]


def find_opa_details(lot):
    data = get_address_data(lot.address_line1)
    if not data: return
    account = data['account_information']
    account_details = data['account_details']

    owner_names = ', '.join(account['owners'])
    owner, created = Owner.objects.get_or_create(
        name=html_unescape(owner_names),
    )

    billing_account, created = BillingAccount.objects.get_or_create(
        external_id=account['account_number'],

        defaults={
            'property_address': account['address'],

            # TODO NB: if starts with 'VAC LAND', could indicate vacancy
            'improvement_description': account_details['improvement_desc'],
            'sale_date': datetime.strptime(account_details['sale_date'], SALE_DATE_FORMAT),
            'land_area': float(account_details['land_area'].split()[0]),

            # TODO NB: if 0, could indicate vacancy
            'improvement_area': float(account_details['improvement_area'].split()[0]),

            # TODO NB: if 0, could indicate publicly owned?
            'assessment': str(account_details['assessment']).translate(None, '$,'),

            'mailing_name': html_unescape(account['mailing_address']['street'][0]),
            'mailing_address': html_unescape(account['mailing_address']['street'][1]),

            'mailing_city': html_unescape(account['mailing_address']['city']),
            'mailing_state_province': html_unescape(account['mailing_address']['state']),
            'mailing_postal_code': html_unescape(account['mailing_address']['zip']),
        },
    )

    if owner.billing_accounts.filter(external_id=billing_account.external_id).count() == 0:
        owner.billing_accounts.add(billing_account)

    lot.billing_account = billing_account
    lot.owner = owner
    lot.save()

    print data
