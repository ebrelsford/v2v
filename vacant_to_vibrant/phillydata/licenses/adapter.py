import logging

import reversion

from phillydata.li.adapter import get_location
from .api import LILicenseReader
from .models import Contact, License, LicenseType


logger = logging.getLogger(__name__)


def find_licenses(code, since):
    reader = LILicenseReader()
    for license in reader.get(code, since=since):
        try:
            saved_license = save_license(license)
            logger.debug('Added license: %s' % saved_license)
        except Exception:
            logger.exception('Failed to load license: %s' % license)


def get_license_type(license):
    license_type, created = LicenseType.objects.get_or_create(
        code=license['license_type_code'],
        name=license['license_type_name'],
    )
    return license_type


def get_contact(license):
    get_fields = {
        'contact_type': 'pri_contact_type',
        'company_name': 'pri_contact_company_name',
        'first_name': 'pri_contact_first_name',
        'last_name': 'pri_contact_last_name',
        'address1': 'pri_contact_address1',
        'address2': 'pri_contact_address2',
        'city': 'pri_contact_city',
        'state': 'pri_contact_state',
        'zip_code': 'pri_contact_zip',
    }
    contact, created = Contact.objects.get_or_create(
        **dict([(k, license[v]) for k, v in get_fields.items()])
    )
    return contact


@reversion.create_revision()
def save_license(license):
    defaults = {
        'location': get_location(license),
        'primary_contact': get_contact(license),
        'issued_datetime': LILicenseReader.parse_datetime(license.get('issued_datetime', None)),
        'inactive_datetime': LILicenseReader.parse_datetime(license.get('inactive_datetime', None)),
        'expires_month': license.get('expires_month', '').strip().title(),
        'expires_year': license['expires_year'],
        'status': license['status'],
    }

    saved_license, created = License.objects.get_or_create(
        external_id=license['license_number'],
        license_type=get_license_type(license),
        defaults=defaults,
    )
    return saved_license
