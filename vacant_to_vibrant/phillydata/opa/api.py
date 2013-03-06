import json
from urllib import quote_plus
from urllib2 import urlopen


BASE_URL = 'http://api.phillyaddress.com/'
ADDRESS_ENDPOINT = 'address/'
ACCOUNT_ENDPOINT = 'account/'


def get_address_data(address):
    # TODO be more defensive
    try:
        url = BASE_URL + ADDRESS_ENDPOINT + quote_plus(address)
        # TODO urllib2 exceptions
        data = json.load(urlopen(url, None, 30))
        return data['property']
    except KeyError:
        print ('Could not find property in response for %s. Trying by account '
               'number') % address

        # Try to find a matching property in the response's properties
        if 'properties' in data:
            for prop in data['properties']:
                if prop['address'].lower() == address.lower():
                    return get_account_data(prop['account_number'])

        return None


def get_account_data(account):
    try:
        url = BASE_URL + ACCOUNT_ENDPOINT + account
        data = json.load(urlopen(url))
        return data['property']
    except Exception:
        print 'There was an exception while getting OPA data for account', account
        return None
