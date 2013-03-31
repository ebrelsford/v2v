from django.test import TestCase

import adapter
from .models import BillingAccount


class AdapterTest(TestCase):

    record = {
        u'account_information': {
            u'owners': [u'PERSON\'S NAME'],
            u'zip': u'19139-0000',
            u'mailing_address': {
                u'city': u'PHILADELPHIA',
                u'state': u'PA',
                u'street': [u'PERSON\'S NAME', u'2616 S ISEMINGER ST'],
                u'zip': u'19148-4320'
            },
            u'account_number': u'441347500',
            u'address': u'453 DEARBORN ST',
            u'unit_number': u''
        },
        u'valuation_details': {
            u'2007': {
                u'market_value': u'$2,000',
                u'gross_tax': u'$52.89',
                u'assessed_improvement_taxable': u'$0',
                u'total_assessment': u'$640',
                u'assessed_improvement_exempt': u'$0',
                u'year': u'2007',
                u'assessed_land_taxable': u'$640',
                u'assessed_land_exempt': u'$0'
            },
            u'2014': {
                u'market_value': u'$3,500',
                u'gross_tax': u'\xa0',
                u'assessed_improvement_taxable': u'$0',
                u'total_assessment': u'$3,500',
                u'assessed_improvement_exempt': u'$0',
                u'year': u'2014',
                u'assessed_land_taxable': u'$3,500',
                u'assessed_land_exempt': u'$0'},
            },
        u'account_details': {
            u'improvement_area': u'0 SqFt',
            u'council_district': u'03',
            u'assessed_improvement_taxable': u'$0',
            u'sale_date': u'2/8/1943',
            u'assessment': u'$640',
            u'begin_point': u'106\' 6" N ASPEN ST',
            u'zoning': u'R9A',
            u'real_estate_tax': u'$62.53',
            u'land_area': u'792.96 SqFt',
            u'assessed_land_taxable': u'$640',
            u'zoning_desc': u'Single Family Row and Twin',
            u'assessed_improvement_exempt': u'$0',
            u'ext_condition': u'\xa0',
            u'market_value': u'$2,000',
            u'sale_price': u'$1',
            u'assessed_land_exempt': u'$0',
            u'improvement_desc': u'VAC LAND RES'
        }
    }

    def test_billing_account_kwargs(self):
        """
        Sanity test for adapter.billing_account_kwargs()
        """
        kwargs = adapter.billing_account_kwargs(self.record)
        self.assertIn('external_id', kwargs)
        self.assertEqual(
            kwargs['external_id'],
            self.record['account_information']['account_number']
        )

    def test_billing_account_defaults(self):
        """
        Sanity test for adapter.billing_account_defaults()
        """
        defaults = adapter.billing_account_defaults(self.record)
        for default in ('improvement_area', 'assessment'):
            self.assertIn(default, defaults)

    def test_get_address(self):
        """
        Sanity test for adapter.get_address()
        """
        address = adapter.get_address(self.record)
        for key in ('mailing_address', 'mailing_city',
                    'mailing_state_province'):
            self.assertIn(key, address)

    def test_get_or_create_account_owner(self):
        """
        Sanity test for adapter.get_or_create_account_owner()
        """
        account_owner = adapter.get_or_create_account_owner(self.record)
        self.assertIsNotNone(account_owner.owner)

    def test_get_or_create_billing_account(self):
        """
        Sanity test for adapter.get_or_create_billing_account()
        """
        account_owner = adapter.get_or_create_account_owner(self.record)
        billing_account = adapter.get_or_create_billing_account(self.record,
                                                                account_owner)
        self.assertEqual(billing_account.external_id,
                         self.record['account_information']['account_number'])
