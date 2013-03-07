import json
from urllib import urlencode
from urllib2 import urlopen, URLError
import traceback


class ArcGISRestServerReader(object):
    """
    A simple class for iterating over objects stored in an ArcGIS server.

    """
    default_params = {
        'f': 'json',
    }

    ids_params = {
        'returnIdsOnly': 'true'
    }

    objects_params = {
        'outFields': '*',
        'outSR': '4326',
    }

    def __init__(self, service_url, geometry_type, geometry, where=[]):
        self.service_url = service_url
        self.default_params.update({
            'geometry': geometry,
            'geometryType': geometry_type,
        })
        self.where = where

    def __iter__(self):
        self.ids = self.get_object_ids()
        return self.get_all()

    def get_object_ids(self):
        """
        Get all object IDs available for this service.

        """
        params = self.default_params.copy()
        params.update(self.ids_params)
        if self.where:
            params.update({
                'where': ' and '.join(self.where),
            })
        url = self.service_url + urlencode(params)
        print 'Getting object ids with url %s' % url
        data = json.load(urlopen(url))
        return data['objectIds']

    def get_all(self, page_size=50):
        """
        Iterate over all available objects for this service.

        """
        for offset in range(0, len(self.ids), page_size):
            page = self.get_objects(offset=offset, count=page_size)
            for feature in page:
                yield feature

    def get_objects(self, offset=0, count=500):
        """
        Get objects in a paginatable way.

        """
        params = self.default_params.copy()
        params.update(self.objects_params)
        params.update({
            'objectIds': ','.join([str(id) for id in self.ids[offset:(offset + count)]]),
        })
        if self.where:
            params.update({
                'where': ' and '.join(self.where),
            })

        url = self.service_url + urlencode(params)
        print 'Getting objects with url', url

        try:
            data = json.load(urlopen(url))
            for feature in data['features']:
                yield feature
        except URLError:
            print 'URLError while fetching url:', url
            traceback.print_stack()
            raise
