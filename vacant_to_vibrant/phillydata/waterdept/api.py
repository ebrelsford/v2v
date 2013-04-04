import json
import logging
from urllib import urlencode
from urllib2 import urlopen

from phillydata.utils import to_point


logger = logging.getLogger(__name__)

BASE_URL = 'http://www.phila.gov/water/swmap/handlers/identify.ashx?'
'x=2692794.2006038&y=236725.2439752'


def get_point_data(lon, lat):
    """Get water department data for the given longitude and latitude."""
    x, y = to_point(lon, lat)
    try:
        url = BASE_URL + urlencode({ 'x': x, 'y': y })
        data = json.load(urlopen(url))
        return data[0]
    except Exception:
        logger.exception('Could not find Water Department records for %f, %f' %
                         (lon, lat))
        return None
