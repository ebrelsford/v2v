import json
import logging
from urllib import quote_plus
from urllib2 import urlopen, URLError

logger = logging.getLogger(__name__)


BASE_URL = 'http://api.phillyaddress.com/'
ADDRESS_ENDPOINT = 'address/'
ACCOUNT_ENDPOINT = 'account/'


def get_address_data(address):
    try:
        url = BASE_URL + ADDRESS_ENDPOINT + quote_plus(address)
        data = json.load(urlopen(url, None, 30))
        return data['property']
    except KeyError:
        logger.debug(('Could not find property in response for %s. Trying by '
                      'account number') % address)

        # Try to find a matching property in the response's properties
        if 'properties' in data:
            for prop in data['properties']:
                if prop['address'].lower() == address.lower():
                    return get_account_data(prop['account_number'])

        logger.debug('Could not find property by account number, either.')
        return None
    except URLError:
        logger.exception('Exception while querying OPA API with URL "%s"' %
                         url)


def get_account_data(account):
    try:
        url = BASE_URL + ACCOUNT_ENDPOINT + account
        data = json.load(urlopen(url))
        return data['property']
    except Exception:
        logger.exception('Exception while getting OPA data for account %s'
                         % str(account))
        return None
