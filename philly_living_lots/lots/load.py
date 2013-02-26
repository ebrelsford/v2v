"""
Utilities for loading lots, mostly from other models.

"""

from datetime import datetime

from .models import Lot
from phillydata.availableproperties.models import AvailableProperty
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
        parcel = find_parcel(violation.violation_location.point,
                             violation.violation_location.address)
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


def load_lots_available(added_after=None):
    # TODO abstract this a bit?
    properties = AvailableProperty.objects.all()
    if added_after:
        properties = properties.filter(added__gte=added_after)
    for available_property in properties:
        parcel = find_parcel(available_property.centroid,
                             mapreg=available_property.mapreg)
        if not parcel:
            print 'No parcel found for available property:', available_property
            continue

        lot, created = Lot.objects.get_or_create(
            address_line1=available_property.address,

            defaults={
                'parcel': parcel,
                'centroid': available_property.centroid,
                'polygon': parcel.geometry,
                'city': 'Philadelphia',
                'state_province': 'PA',
                'country': 'USA',
            },
        )
        lot.available_property = available_property
        lot.save()


def find_parcel(point, address=None, mapreg=None):
    # TODO couldn't this be in phillydata.parcels.* ?
    parcels = Parcel.objects.filter(
        geometry__contains=point,
    )
    if parcels.count() > 1:
        print 'Found an unexpected number of parcels (%d) for point' % parcels.count(), point
        if address:
            print 'Trying to filter by address: "%s"' % address
            parcels = parcels.filter(address=address)
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


def find_opa_details(lot):
    # TODO shouldn't this be in phillydata.opa.* ?
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
