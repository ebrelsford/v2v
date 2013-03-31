from django.test import TestCase

import adapter


class AdapterTest(TestCase):

    land_use_area = {
        u'geometry': {
            u'rings': [[
                [-75.24506159442592, 39.91870995604932],
                [-75.24496036237824, 39.918625099944656],
                [-75.24495932392577, 39.91862424837913],
                [-75.24470461291516, 39.91841190992015],
                [-75.2448334546831, 39.918321796590874],
                [-75.24483451289849, 39.91832267503],
                [-75.24500408338311, 39.918203699129506],
                [-75.24507360849452, 39.91815491912968],
                [-75.2450809369506, 39.918149777319755],
                [-75.24508200235253, 39.91814984828406],
                [-75.24508112020693, 39.91815047387211],
                [-75.24509413499875, 39.91816136861089],
                [-75.24524258878598, 39.91828566482884],
                [-75.2454554643555, 39.91846616429615],
                [-75.24521153222999, 39.918635893329494],
                [-75.24539827940114, 39.91878761578683],
                [-75.24537740435058, 39.9188028357595],
                [-75.24526920407122, 39.9188797478633],
                [-75.24526778832634, 39.9188808440086],
                [-75.24506159442592, 39.91870995604932]
            ]]},
        u'attributes': {
            u'C_DIG2DESC': u'Vacant',
            u'SHAPE_Length': 298.28936621109244,
            u'SHAPE_Area': 4095.58814847389,
            u'VACBLDG': None,
            u'OBJECTID': 18439,
            u'C_DIG1DESC': u'Vacant or Other',
            u'C_DIG3DESC': u'Vacant Parcels',
            u'C_DIG1': 9,
            u'C_DIG2': 91,
            u'C_DIG3': 911,
            u'EDIT_ATTRIB': None,
            u'EDIT_FEAT': None
        }
    }

    def test_model_get_kwargs(self):
        """
        Sanity test for adapter.model_get_kwargs()
        """
        kwargs = adapter.model_get_kwargs(self.land_use_area)
        self.assertIn('object_id', kwargs)
        self.assertEqual(kwargs['object_id'],
                         self.land_use_area['attributes']['OBJECTID'])

    def test_model_defaults(self):
        """
        Sanity test for adapter.model_defaults()
        """
        defaults = adapter.model_defaults(self.land_use_area)
        for default in ('geometry', 'category', 'subcategory',):
            self.assertIn(default, defaults)

    def test_create(self):
        """
        Test creation using adapter.create_or_update()
        """
        saved_model = adapter.create_or_update(self.land_use_area)
        self.assertEqual(saved_model.category,
                         self.land_use_area['attributes']['C_DIG1DESC'])

    def test_update(self):
        """
        Test update using adapter.create_or_update()
        """
        created_model = adapter.create_or_update(self.land_use_area)
        updated_model = adapter.create_or_update(self.land_use_area)
        self.assertEqual(updated_model.category,
                         self.land_use_area['attributes']['C_DIG1DESC'])
