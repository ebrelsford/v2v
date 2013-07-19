import csv
from datetime import datetime
import itertools

from django.conf import settings

from libapps.organize.models import OrganizerType
from lots.models import Lot, LotGroup, Use
from phillydata.parcels.models import Parcel
from phillydata.utils import fix_address
from phillydata.zoning.models import BaseDistrict
from phillyorganize.models import Organizer
from steward.models import StewardProject


# Basereg pattern [^-]{6}-[^-]{4}
# Some Baseregs are doubled up

def find_lot(basereg, address):
    try:
        return Lot.objects.get(parcel__basereg=basereg)
    except Exception:
        try:
            return Lot.objects.get(
                address_line1__iexact=address,
                parcel__basereg=basereg,
            )
        except Exception:
            return None


def find_parcel(basereg, address):
    """Try to find a parcel and create a lot"""
    try:
        return Parcel.objects.get(basereg=basereg)
    except Exception:
        try:
            return Parcel.objects.get(address__iexact=address)
        except Exception:
            return None


def create_lot(basereg, address, **defaults):
    parcel = find_parcel(basereg, address)
    if not parcel:
        return None
    polygon = parcel.geometry
    centroid = polygon.centroid
    lot = Lot(
        centroid=centroid,
        polygon=polygon,
        parcel=parcel,
        **defaults
    )
    lot.polygon_area = lot.calculate_polygon_area()
    lot.polygon_width = lot.calculate_polygon_width()
    try:
        lot.zoning_district = BaseDistrict.objects.get(
            geometry__contains=lot.centroid,
        )
    except (BaseDistrict.DoesNotExist, BaseDistrict.MultipleObjectsReturned):
        pass
    lot.save()
    return lot


def to_basereg(s):
    return s.replace('-', '')


def find_or_create_lot(row):
    basereg = to_basereg(row['BaseReg'])
    address = fix_address(row['INDIVIDUAL_PARCEL'])

    # Try to find the parcel as a Lot
    lot = find_lot(basereg, address)

    # If that fails find it as a Parcel, and create a Lot for it
    if not lot:
        # Let OPASynchronizer handle ownership data
        defaults = {
            'address_line1': address,
            'city': 'Philadelphia',
            'state_province': 'PA',
            'postal_code': row['ZIP'],
        }
        lot = create_lot(basereg, address, **defaults)
    return lot


def parse_datetime(s):
    try:
        return datetime.strptime(s, '%m/%d/%Y')
    except Exception:
        return None


def load(filename=settings.DATA_ROOT + '/gardens.csv',
         create_organizers=False, append_to_existing=False):
    reader = csv.DictReader(open(filename, 'r'))

    gardens = itertools.groupby(reader, lambda r: r['GARDEN NAME'])

    # Default organizer type and use for all gardens
    organizer_type = OrganizerType.objects.get(name__exact='community based organization')
    steward_project_use = Use.objects.get(name__exact='community garden')

    for garden, parcels in gardens:
        lots = []
        lotgroup_kwargs = {
            'city': 'Philadelphia',
            'state_province': 'PA',
            'known_use': steward_project_use,
            'known_use_certainty': 7,
            'known_use_locked': True,
            'steward_inclusion_opt_in': True,
        }
        organizer_kwargs = {
            'type': organizer_type,
        }
        steward_kwargs = {
            'use': steward_project_use,
            'include_on_map': True,
        }

        for parcel in parcels:
            lotgroup_kwargs.update({
                'name': (fix_address(parcel['GARDEN NAME']) or
                         lotgroup_kwargs.get('name', None)),
                'address_line1': (fix_address(parcel['ADDRESS']) or
                                  lotgroup_kwargs.get('address_line1', None)),
                'postal_code': (parcel['ZIP'] or
                                lotgroup_kwargs.get('postal_code', None)),
            })
            organizer_kwargs.update({
                'name': (parcel['Main Contact'] or
                         organizer_kwargs.get('name', None)),
                'phone': (parcel['Phone Number'] or
                          organizer_kwargs.get('phone', None)),
                'email': (parcel['Email Address'] or
                          organizer_kwargs.get('email', None)),
            })
            steward_kwargs.update({
                'name': fix_address(parcel['GARDEN NAME']) or steward_kwargs.get('name', None),
                'support_organization': (parcel['Support Organization'] or
                                         organizer_kwargs.get('support_organization', None)),
                'external_id': (parcel['PROJECT ID'] or
                                steward_kwargs.get('external_id', None)),
                'date_started': (parse_datetime(parcel['DATESTARTED']) or
                                 steward_kwargs.get('date_started', None)),
            })

            lot = find_or_create_lot(parcel)
            if lot:
                lots.append(lot)

        print 'Trying to add garden "%s"' % lotgroup_kwargs['name']
        if not lots:
            print 'No lots found, skipping garden "%s"' % lotgroup_kwargs['name']
            continue

        print 'lotgroup_kwargs', lotgroup_kwargs
        print 'organizer_kwargs', organizer_kwargs
        print 'steward_kwargs', steward_kwargs

        if append_to_existing:
            # Try to find existing steward project
            try:
                steward_project = StewardProject.objects.get(
                    name=steward_kwargs['name']
                )
            except Exception:
                steward_project = None

        if steward_project:
            # Look for steward_project's LotGroup
            try:
                lot_group = steward_project.content_object.lotgroup
            except Exception:
                # Create new LotGroup
                lot_group = LotGroup(**lotgroup_kwargs)
                lot_group.save()
                # Swap the steward project's old lot with the new group
                steward_project.content_object.group = lot_group
                steward_project.content_object.save()
                steward_project.content_object = lot_group
                steward_project.save()
            for member_lot in lots:
                member_lot.group = lot_group
                member_lot.save()
        else:
            # Group Lots (if len > 1)
            if len(lots) > 1:
                lot = LotGroup(**lotgroup_kwargs)
                lot.save()
                for member_lot in lots:
                    member_lot.group = lot
                    member_lot.save()
            else:
                lot = lots[0]

            if create_organizers and organizer_kwargs['name'] and organizer_kwargs['email']:
                organizer = Organizer(content_object=lot, **organizer_kwargs)
                organizer.save()
            else:
                organizer = None

            # Create a StewardProject for the (group of) lots
            steward_project = StewardProject(
                content_object=lot,
                organizer=organizer,
                **steward_kwargs
            )
            steward_project.save()
