import json

from django.test import TestCase

from .api import get_point_data
from .adapter import (_get_or_create_water_parcel,
                      _get_or_create_water_accounts, _water_account_defaults,
                      _water_account_kwargs, _water_parcel_defaults,
                      _water_parcel_kwargs)


class ApiTest(TestCase):
    """Tests the API."""

    def test_success(self):
        """Tests the API with a valid lon/lat pair."""
        data = get_point_data(-75.125033, 40.001885)
        self.assertIsNotNone(data)
        self.assertIn('Accounts', data)
        self.assertIn('Parcel', data)

    def test_failure(self):
        """Tests the API with an invalid (ie, outside Philly) lon/lat pair."""
        data = get_point_data(0, 0)
        self.assertIsNone(data)


class AdapterTest(TestCase):
    """Tests the adapter."""

    record = {
        "MinCharge": False,
        "Parcel": {
            "Owner1": "OWNER NAME",
            "ImpervCredit": 0,
            "BRTAcct": "123456789",
            "Owner2": None,
            "FinalImperv": 500,
            "FinalGross": 1000,
            "GrossArea": 968,
            "BldgType": "NonRes",
            "NPDESCredit": 0,
            "ParcelID": 123456,
            "TenCode": "1234567890",
            "Shape": "POLYGON ((2703814.74156681 254477.754747897, 2703813.02798755 254463.902413398, 2703743.47825789 254472.777067557, 2703745.30371356 254486.647118554, 2703814.74156681 254477.754747897))",
            "ImpervArea": 242,
            "Address": "1234 ABC ST",
            "GrossCredit": 0,
            "BldgDesc": "VAC LAND RES 003c ACRE",
            "BldgCode": "SR"
        },
        "Area": 978.986368503422,
        "Length": 168.066160089772,
        "Accounts": [
            {
                "AccountStatusAbbrev": "D",
                "WaterAccount": "0987654321234",
                "HouseNum": "1234",
                "ControlDay": "023",
                "ServiceTypeLabel": "R - (no description)",
                "Fire": "N",
                "InstID": 123456,
                "StormwaterStatus": "Not Billed",
                "MeterSizeAbbrev": None,
                "ParcelID": 123456,
                "ServiceType": "3R",
                "AccountNumber": "023-09876-54321-234",
                "TenCode": "1234567890",
                "AcctStatus": "Discontinued",
                "StreetDir": None,
                "MeterSize": "(no description)",
                "NonBillCode": "NB5",
                "CustomerID": 654321,
                "StreetName": "ABC ST",
                "CustomerName": None
            },
            {
                "AccountStatusAbbrev": "C",
                "WaterAccount": "0987654321235",
                "HouseNum": "1234",
                "ControlDay": "023",
                "ServiceTypeLabel": "3 - Stormwater Only",
                "Fire": "N",
                "InstID": 123456,
                "StormwaterStatus": "Billed",
                "MeterSizeAbbrev": "A",
                "ParcelID": 123456,
                "ServiceType": "43A",
                "AccountNumber": "023-09876-54321-234",
                "TenCode": "1234567890",
                "AcctStatus": "Current",
                "StreetDir": None,
                "MeterSize": "No Meter",
                "NonBillCode": None,
                "CustomerID": 123456,
                "StreetName": "ABC ST",
                "CustomerName": "CUSTOMERNAME"
            }
        ],
        "Y": 254475.274765976,
        "X": 2703779.12088409,
        "BufferedEnvelope": {
            "XMin": 2703725.66243066,
            "YMin": 254458.216237109,
            "YMax": 254492.333294843,
            "XMax": 2703832.55739404
        },
        "Match": {
            "Type": "XY",
            "Value": [
                2703782.91588,
                254472.639808
            ]
        },
        "ImprvCount": 0
    }

    def test_parcel_kwargs(self):
        kwargs = _water_parcel_kwargs(self.record)
        self.assertIsNotNone(kwargs)
        self.assertEqual(123456, kwargs['parcel_id'])

    def test_parcel_defaults(self):
        defaults = _water_parcel_defaults(self.record)
        self.assertIsNotNone(defaults)

    def test_account_kwargs(self):
        for account in self.record['Accounts']:
            kwargs = _water_account_kwargs(account)
            self.assertIsNotNone(kwargs)

    def test_account_defaults(self):
        for account in self.record['Accounts']:
            defaults = _water_account_defaults(account)
            self.assertIsNotNone(defaults)

    def test_get_or_create_water_parcel(self):
        water_parcel = _get_or_create_water_parcel(self.record)
        self.assertIsNotNone(water_parcel)

    def test_get_or_create_water_accounts(self):
        water_parcel = _get_or_create_water_parcel(self.record)
        water_accounts = _get_or_create_water_accounts(self.record, water_parcel)
        self.assertIsNotNone(water_accounts)
        self.assertNotEqual(0, len(water_accounts))
