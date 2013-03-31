from django.test import TestCase

import adapter
from .models import AvailableProperty


class AdapterTest(TestCase):

    available_property = {
        u'geometry': {u'y': 39.9664, u'x': -75.2079},
        u'attributes': {
            u'ASSET_ID': 14208,
            u'OBJECTID': 35851,
            u'DESCR': None,
            u'MAPREG': u'057N020246',
            u'AGENCY': u'PUB',
            u'ZONING': u'C2',
            u'PRICE_STR': u'$6,431.00',
            u'REF_ADDRES': u'4208 Lancaster Ave',
            u'SQFEET': 992.4,
            u'IMG_URL': None,
            u'PRICE': 6431
        }
    }

    def test_model_get_kwargs(self):
        """
        Sanity test for adapter.model_get_kwargs()
        """
        kwargs = adapter.model_get_kwargs(self.available_property)
        self.assertIn('asset_id', kwargs)
        self.assertEqual(kwargs['asset_id'],
                         self.available_property['attributes']['ASSET_ID'])

    def test_model_defaults(self):
        """
        Sanity test for adapter.model_defaults()
        """
        defaults = adapter.model_defaults(self.available_property)
        for default in ('centroid', 'mapreg', 'agency'):
            self.assertIn(default, defaults)

    def test_create(self):
        """
        Test creation using adapter.create_or_update()
        """
        saved_model = adapter.create_or_update(self.available_property)
        self.assertEqual(saved_model.status, AvailableProperty.STATUS_NEW)

    def test_update(self):
        """
        Test update using adapter.create_or_update()
        """
        created_model = adapter.create_or_update(self.available_property)
        updated_model = adapter.create_or_update(self.available_property)
        self.assertEqual(updated_model.status,
                         AvailableProperty.STATUS_AVAILABLE)
