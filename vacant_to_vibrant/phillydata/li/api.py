from odata.reader import ODataReader
from phillydata import utils


class LIReader(ODataReader):

    service_url = 'http://services.phila.gov/PhillyApi/Data/v0.7/Service.svc/'

    def __init__(self):
        pass

    @classmethod
    def get_lon_lat(cls, location):
        (x, y) = (location['x'], location['y'])
        if not x or not y: return (None, None)
        (x, y) = [float(coord) for coord in (x, y)]
        return utils.to_lon_lat(x, y)

    @classmethod
    def make_address(cls, location):
        return utils.make_address(
            house_number=location['street_number'],
            street_direction=location['street_direction'],
            street_name=location['street_name'],
            street_description=location['street_suffix'],
        )
