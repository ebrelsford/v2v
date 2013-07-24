from datetime import datetime
from dateutil.tz import tzlocal
import json
import logging
import re
from urllib import urlencode
from urllib2 import urlopen

DATETIME_REGEX = re.compile('\D*(\d+)\D*')
logger = logging.getLogger(__name__)


class ODataReader(object):

    def __init__(self, service_url):
        self.service_url = service_url

    def get(self, endpoint, params={}):
        """
        Get data from the given service and endpoint.

        """
        params.update({ '$format': 'json' })
        url = self.service_url + endpoint + '?' + urlencode(params)
        return self.get_url(url)

    def get_url(self, url):
        while True:
            # load this url and return results
            logger.debug('About to load OData source from url %s' % url)

            attempts = 0
            while attempts < 5:
                attempts += 1
                try:
                    logger.debug('Attempt #%d to load url %s' %
                                 (attempts, url))
                    response = json.load(urlopen(url))
                    break
                except Exception:
                    # Don't bother with looking at HTTP error code: some
                    # services have returned 500 once, then responded
                    # successfully after
                    logger.exception('Exception while loading url: %s' % url)
            if not response:
                logger.warn('No response after %d attempts' % attempts)
                raise StopIteration

            for result in response['d']['results']:
                yield result

            # try to load next url for pagination
            try:
                url = response['d']['__next']
                url += '&' + urlencode({ '$format': 'json' })
            except KeyError:
                raise StopIteration

    @classmethod
    def parse_datetime(cls, timestamp):
        """Parse a datetime from an OData feed."""
        if not timestamp: return None
        timestamp = re.match(DATETIME_REGEX, timestamp).group(1)
        return datetime.fromtimestamp(float(timestamp[:-3]), tzlocal())

    @classmethod
    def format_datetime(cls, dt):
        """Format a datetime into a form recognized in OData filters."""
        return "DateTime'%s'" % datetime.isoformat(dt.replace(microsecond=0))
