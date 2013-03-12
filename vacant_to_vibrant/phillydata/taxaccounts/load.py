"""
Utilities for loading tax data.

"""
import csv
import os
import traceback

from django.conf import settings

from .adapter import create_or_update_tax_account


#TAX_DELINQUENCY_DATA_FILE = os.path.join(settings.DATA_ROOT,
                                         #'201206_delinquencies_vacantLand.csv')

TAX_DELINQUENCY_DATA_FILE = os.path.join(settings.DATA_ROOT,
                                         '201206_delinquencies.csv')


def _save_entry(entry):
    # All data in file is from this date
    override = {
        'last_updated': '2012-06-01',
    }
    return create_or_update_tax_account(entry, override=override)


def load_tax_data(source=TAX_DELINQUENCY_DATA_FILE):
    entries = csv.DictReader(open(source, 'r'))
    for entry in entries:
        try:
            _save_entry(entry)
        except Exception:
            print 'Could not save tax entry %s. Skipping.' % entry
            traceback.print_exc()
