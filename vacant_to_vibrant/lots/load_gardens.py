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


def find_or_create_lot(address, basereg, zip):
    # Try to find the parcel as a Lot
    lot = find_lot(basereg, address)

    # If that fails find it as a Parcel, and create a Lot for it
    if not lot:
        # Let OPASynchronizer handle ownership data
        defaults = {
            'address_line1': address,
            'city': 'Philadelphia',
            'state_province': 'PA',
            'postal_code': zip,
        }
        lot = create_lot(basereg, address, **defaults)
    return lot


def find_or_create_lots(row, address=None):
    raw_address = (row.get('INDIVIDUAL_PARCEL', None) or
                   row.get('ADDRESS', None) or
                   address)
    address = fix_address(raw_address)
    lots = []
    for basereg_raw in row['BaseReg'].split(','):
        basereg = to_basereg(basereg_raw.strip())
        lot = find_or_create_lot(address, basereg, row['ZIP'])
        if lot:
            lots += (lot,)
    return lots


def find_or_create_lotgroup(parcels, address=None, **lotgroup_defaults):
    """
    Find or create a LotGroup for the given parcels. If there is only one lot
    in the parcels, just return that lot.
    """
    lots = []
    lotgroup = None
    for parcel in parcels:
        parcel_lots = find_or_create_lots(parcel, address=address)
        for lot in parcel_lots:
            if lot.group:
                lotgroup = lot.group
        lots += parcel_lots

    if len(lots) > 1:
        if lotgroup:
            lot = lotgroup
        else:
            lot = LotGroup(**get_lotgroup_kwargs(address=address,
                                                 **lotgroup_defaults))
            lot.save()
        for member_lot in lots:
            member_lot.group = lot
            member_lot.save()
        return lot
    elif len(lots) == 1:
        lot = lots[0]
        # Intentionally don't get the address, trust the parcel's
        kwargs = get_lotgroup_kwargs(**lotgroup_defaults)
        Lot.objects.filter(pk=lot.pk).update(**kwargs)
        return lot
    return None


def load_final_gardens(filename):
    gardens_reader = csv.DictReader(open(filename, 'r'))
    gardens = []
    for garden in gardens_reader:
        if garden['Garden exists?'].lower() == 'not a garden':
            continue
        gardens.append({
            'pilcop code': garden['PILCOP GARDEN code'],
            'name': garden['Garden Name (DO NOT EDIT  - from Garden Code)'],
            'address': garden['Address (DO NOT EDIT - from GARDEN CODE)'],
            'zip': garden['ZIP - should be deleted in exchange for parcel information'],
        })
    return gardens


def load_final_parcels(filename):
    reader = csv.DictReader(open(filename, 'r'))
    return itertools.groupby(reader, lambda p: p['pilcop garden code'])


def parse_datetime(s):
    try:
        return datetime.strptime(s, '%m/%d/%Y')
    except Exception:
        return None


def get_lotgroup_kwargs(name=None, address=None, zip=None):
    kwargs = {
        'city': 'Philadelphia',
        'state_province': 'PA',
        'known_use': Use.objects.get(name__exact='community garden'),
        'known_use_certainty': 7,
        'known_use_locked': True,
        'steward_inclusion_opt_in': True,
    }
    if name:
        kwargs['name'] = name
    if address:
        kwargs['address_line1'] = address
    if zip:
        kwargs['postal_code'] = zip
    return kwargs


def get_steward_kwargs(name=None, support_organization=None,
                       pilcop_garden_id=None):
    kwargs = {
        'use': Use.objects.get(name__exact='community garden'),
        'include_on_map': True,
    }
    if name:
        kwargs['name'] = name
    if support_organization:
        kwargs['support_organization'] = support_organization
    if pilcop_garden_id:
        kwargs['pilcop_garden_id'] = pilcop_garden_id
    return kwargs


def find_garden(gardens, code):
    for g in gardens:
        if g['pilcop code'] == code:
            return g
    return None


def get_support_organization(parcels):
    for parcel in parcels:
        support_organization = parcel.get('Support Organization', None)
        if support_organization:
            return support_organization
    return None


def load_final_db(gardens_filename=settings.DATA_ROOT + '/final_gardens.csv',
                  parcels_filename=settings.DATA_ROOT + '/final_parcels.csv'):
    """
    Load the "final" garden database created by PILCOP.

    Gardens and their parcels are kept in separate files. Group parcels by
    garden and add or update steward projects for each.

    This is basically a one-off script for loading the database and will likely
    be modified for future versions of the database.
    """
    gardens = load_final_gardens(gardens_filename)

    for garden_code, parcels in load_final_parcels(parcels_filename):
        garden = find_garden(gardens, garden_code)

        if not garden:
            print ('%s: Could not find garden (maybe it is marked "not a ' +
                   'garden?". Skipping.') % garden_code
            continue

        lot = find_or_create_lotgroup(parcels,
            address=garden['address'],
            name=garden['name'],
            zip=garden['zip']
        )
        if not lot:
            print '%s: Could not find lot for parcels. Skipping.' % garden_code
            continue

        steward_kwargs = get_steward_kwargs(
            name=garden['name'],
            support_organization=get_support_organization(parcels),
            pilcop_garden_id=garden_code,
        )

        if lot.steward_projects.count() > 0:
            steward_project = lot.steward_projects.all()[0]
            print ('%s: Lot already has a steward project, %s. Updating.' %
                   (garden_code, steward_project,))
            StewardProject.objects.filter(pk=steward_project.pk).update(
                **steward_kwargs
            )
            continue

        # Create a StewardProject for the (group of) lots
        print '%s: Lot did not have a steward project. Adding now.' % garden_code
        steward_project = StewardProject(content_object=lot, **steward_kwargs)
        steward_project.save()


def load(filename=settings.DATA_ROOT + '/gardens.csv',
         create_organizers=False, append_to_existing=False):
    reader = csv.DictReader(open(filename, 'r'))

    gardens = itertools.groupby(reader, lambda r: r['GARDEN NAME'])

    # Default organizer type and use for all gardens
    organizer_type = OrganizerType.objects.get(name__exact='community based organization')
    steward_project_use = Use.objects.get(name__exact='community garden')

    for garden, parcels in gardens:
        lots = []
        lotgroup_kwargs = get_lotgroup_kwargs()
        organizer_kwargs = {}
        if create_organizers:
            organizer_kwargs.update({
                'type': organizer_type,
            })
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
            if create_organizers:
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
                'external_id': (parcel.get('PROJECT ID', None) or
                                steward_kwargs.get('external_id', None)),
                'date_started': (parse_datetime(parcel.get('DATESTARTED', None)) or
                                 steward_kwargs.get('date_started', None)),
            })

            lots += find_or_create_lots(parcel)

        print 'Trying to add garden "%s"' % lotgroup_kwargs['name']
        print 'lots:', lots
        if not lots:
            print 'No lots found, skipping garden "%s"' % lotgroup_kwargs['name']
            continue

        print 'lotgroup_kwargs', lotgroup_kwargs
        if create_organizers:
            print 'organizer_kwargs', organizer_kwargs
        print 'steward_kwargs', steward_kwargs

        steward_project = None
        if append_to_existing:
            # Try to find existing steward project
            try:
                steward_project = StewardProject.objects.get(
                    name=steward_kwargs['name']
                )
            except Exception:
                pass

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
