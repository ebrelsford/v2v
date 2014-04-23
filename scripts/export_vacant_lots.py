import csv

from lots.models import Lot


fields = ('address', 'basereg', 'brt number', 'owner name', 'owner type',)

writer = csv.DictWriter(open('vacant_lots.csv', 'w'), fields)

for lot in Lot.objects.filter(known_use=None):
    lotdict = {
        'address': lot.address_line1,
    }
    if lot.parcel:
        lotdict['basereg'] = lot.parcel.basereg
    if lot.tax_account:
        lotdict['brt number'] = lot.tax_account.brt_number
    if lot.owner:
        lotdict['owner name'] = lot.owner.name
        lotdict['owner type'] = lot.owner.owner_type

    writer.writerow(lotdict)
