from re import match

from odata.reader import ODataReader
from phillydata.utils import to_lon_lat


ADDRESS_NUMBERED_STREET_REGEX = '^\d+\w+$'


class LIReader(ODataReader):

    service_url = 'http://services.phila.gov/PhillyApi/Data/v0.7/Service.svc/'

    def __init__(self):
        pass

    @classmethod
    def get_lon_lat(cls, location):
        (x, y) = (location['x'], location['y'])
        if not x or not y: return (None, None)
        (x, y) = [float(coord) for coord in (x, y)]
        return to_lon_lat(x, y)

    @classmethod
    def format_street_name(cls, street_name):
        if match(ADDRESS_NUMBERED_STREET_REGEX, street_name):
            return street_name.lower()
        return street_name.title()

    @classmethod
    def make_address(cls, location):
        components = (
            str(int(location['street_number'])), # chop off leading zeroes
            location['street_direction'].title(),
            cls.format_street_name(location['street_name']),
            location['street_suffix'].title(),
        )
        components = [c.strip() for c in components if c]
        components = filter(lambda c: c and c != '', components)
        return ' '.join(components)


class LIViolationReader(LIReader):

    endpoint = 'violationdetails'

    def get(self, code, year=2013, params={}):
        params.update({
            '$expand': 'locations',
            '$filter': "violation_code eq '%s' and year(violation_datetime) eq %d" % (code, year,),
            'orderby': "violation_datetime desc",
        })
        return super(LIViolationReader, self).get(self.endpoint, params)
