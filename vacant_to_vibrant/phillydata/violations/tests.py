from django.test import TestCase

import adapter


class AdapterTest(TestCase):

    record = {
        u'location': u'5109 W. STILES ST.\r\n5111-13 W. STILES ST.',
        u'violation_code': u'CP-802',
        u'violation_details_id': 2729519,
        u'__metadata': {
            u'type': u'PlanPhillyModel.violationdetails',
            u'uri': u'http://services.phila.gov/PhillyAPI/Data/v0.7/Service.svc/violationdetails(2729519)'
        },
        u'locations': {
            u'council_district': u'03',
            u'zoningboardappeals': {u'__deferred': {u'uri': u'http://services.phila.gov/PhillyAPI/Data/v0.7/Service.svc/locations(690752)/zoningboardappeals'}},
            u'street_name': u'51ST',
            u'census_tract': u'111',
            u'violationdetails': {u'__deferred': {u'uri': u'http://services.phila.gov/PhillyAPI/Data/v0.7/Service.svc/locations(690752)/violationdetails'}},
            u'licenses': {u'__deferred': {u'uri': u'http://services.phila.gov/PhillyAPI/Data/v0.7/Service.svc/locations(690752)/licenses'}},
            u'condo_unit': u'0000000',
            u'location_id': 690752,
            u'cases': {u'__deferred': {u'uri': u'http://services.phila.gov/PhillyAPI/Data/v0.7/Service.svc/locations(690752)/cases'}},
            u'city': u'PHILADELPHIA',
            u'zip': u'19131-4401',
            u'street_suffix': u'ST',
            u'appealhearings': {u'__deferred': {u'uri': u'http://services.phila.gov/PhillyAPI/Data/v0.7/Service.svc/locations(690752)/appealhearings'}},
            u'state': u'PA',
            u'unit_number': u'0000000',
            u'census_block': None,
            u'buildingboardappeals': {u'__deferred': {u'uri': u'http://services.phila.gov/PhillyAPI/Data/v0.7/Service.svc/locations(690752)/buildingboardappeals'}},
            u'lireviewboardappeals': {u'__deferred': {u'uri': u'http://services.phila.gov/PhillyAPI/Data/v0.7/Service.svc/locations(690752)/lireviewboardappeals'}},
            u'ward': u'44',
            u'street_number': u' 01220',
            u'permits': {u'__deferred': {u'uri': u'http://services.phila.gov/PhillyAPI/Data/v0.7/Service.svc/locations(690752)/permits'}},
            u'__metadata': {
                u'type': u'PlanPhillyModel.locations',
                u'uri': u'http://services.phila.gov/PhillyAPI/Data/v0.7/Service.svc/locations(690752)'
            },
            u'y': u'242944',
            u'x': u'2676373',
            u'street_direction': u'N'
        },
        u'violation_code_description': u'DUMPING - PRIVATE LOT',
        u'violation_datetime': u'/Date(1362114000000)/',
        u'case_number': u'371285',
        u'cases': {u'__deferred': {u'uri': u'http://services.phila.gov/PhillyAPI/Data/v0.7/Service.svc/violationdetails(2729519)/cases'}},
        u'location_id': 690752,
        u'violation_status': u'Complied'
    }

    def test_get_location(self):
        location = adapter.get_location(self.record)
        self.assertIsNotNone(location.point)

    def test_get_violation_type(self):
        violation_type = adapter.get_violation_type(self.record)
        self.assertEqual(violation_type.code, self.record['violation_code'])
