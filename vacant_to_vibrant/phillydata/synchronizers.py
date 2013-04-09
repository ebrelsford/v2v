import logging

from inplace.boundaries.models import Boundary

from lots.load import (load_lots_available, load_lots_with_violations,
                       load_lots_land_use_vacant)
from lots.models import Lot
from sync.synchronizers import Synchronizer
from .availableproperties.adapter import (find_available_properties,
                                          find_no_longer_available_properties)
from .landuse.adapter import find_land_use_areas
from .opa.adapter import find_opa_details
from .violations.adapter import find_violations
from .waterdept.adapter import find_water_dept_details
from .zoning.models import BaseDistrict


logger = logging.getLogger(__name__)


class OPASynchronizer(Synchronizer):
    """
    A Synchronizer that updates ownership data using the OPA API.

    """
    def sync(self, data_source):
        logger.info('Starting to synchronize OPA data.')
        self.update_owner_data(count=data_source.batch_size or 1000)
        logger.info('Finished synchronizing OPA data.')

    def update_owner_data(self, count=1000):
        # TODO also lots where the owner has not been touched in a while?
        # eg, last_seen for BillingAccount?

        # grab a random set of lots to update
        lots = Lot.objects.filter(owner__isnull=True).order_by('?')[:count]
        for lot in lots:
            logger.debug('Updating OPA data for lot %s' % lot)
            try:
                lot.billing_account = find_opa_details(lot.address_line1)
                lot.owner = lot.billing_account.account_owner.owner
                lot.save()
            except Exception:
                logger.warn('Caught exception while getting OPA data for lot '
                            '%s' % lot)


class WaterDeptSynchronizer(Synchronizer):
    """
    A Synchronizer that updates Water Department data.

    """
    def sync(self, data_source):
        logger.info('Starting to synchronize Water Department data.')
        self.update_water_dept_data()
        logger.info('Finished synchronizing Water Department data.')

    def update_water_dept_data(self):
        # TODO also lots where the water dept data has not been touched in a while?
        for lot in Lot.objects.filter(water_parcel__isnull=True):
            logger.debug('Updating Water Department data for lot %s' % lot)
            try:
                lot.water_parcel = find_water_dept_details(lot.polygon.centroid.x,
                                                           lot.polygon.centroid.y)
                lot.save()
            except Exception:
                logger.exception('Exception while updating Water Department '
                                 'data for lot %s' % lot)


class LandUseAreaSynchronizer(Synchronizer):
    """Synchronizes LandUseAreas."""

    def sync(self, data_source):
        logger.info('Synchronizing vacant land use area data.')
        find_land_use_areas()
        logger.info('Done synchronizing vacant land use area data.')

        logger.info('Adding lots with vacant land use areas.')
        load_lots_land_use_vacant(added_after=data_source.last_synchronized)
        logger.info('Done adding lots with vacant land use areas.')


class PRAAvailablePropertiesSynchronizer(Synchronizer):
    """
    Attempts to synchronize the local database with the available properties
    as listed by the Philadelphia Redevelopment Authority.

    As the PRA's data does not include timestamps for available properties,
    we load all available properties every time we synchronize, marking new
    ones (status == 'new and available'), existing ones (status ==
    'available'), and properties no longer in the PRA's data (status == 'no
    longer available').

    Once the above is accomplished, we load lots for available properties that
    are new.

    """
    def sync(self, data_source):
        logger.info('Synchronizing available properties.')
        find_available_properties()
        logger.info('Done synchronizing available properties.')

        logger.info('Synchronizing no-longer available properties.')
        find_no_longer_available_properties(data_source.last_synchronized)
        logger.info('Done synchronizing no-longer available properties.')

        logger.info('Adding lots with available properties.')
        load_lots_available(added_after=data_source.last_synchronized)
        logger.info('Done adding lots with available properties.')


class LIViolationsSynchronizer(Synchronizer):
    """
    A Synchronizer that updates L&I Violation data.

    """
    # L&I says these should be the useful codes
    codes = ('CP-802', 'PM-102.4/1', 'PM-302.2/4', 'PM-306.0/2', 'PM-306.0/91',
             'PM-307.1/21',)

    def sync(self, data_source):
        logger.info('Starting to synchronize L&I Violation data.')
        self.update_violation_data()
        logger.info('Finished synchronizing L&I Violation data.')

        logger.info('Adding lots with violations.')
        load_lots_with_violations()
        logger.info('Done adding lots with violations.')

    def update_violation_data(self):
        for code in self.codes:
            find_violations(code, self.data_source.last_synchronized)


class ZoningSynchronizer(Synchronizer):
    """A Synchronizer that updates zoning for lots."""

    def sync(self, data_source):
        logger.info('Starting to synchronize zoning.')
        self.update_zoning(count=data_source.batch_size or 1000)
        logger.info('Finished synchronizing zoning.')

    def update_zoning(self, count=1000):
        lots = Lot.objects.filter(zoning_district__isnull=True).order_by('?')
        for lot in lots[:count]:
            try:
                lot.zoning_district = BaseDistrict.objects.get(
                    geometry__contains=lot.centroid,
                )
                lot.save()
            except Exception:
                logger.warn('Caught exception while updating zoning for lot '
                            '%s' % lot)


class CityCouncilSynchronizer(Synchronizer):
    """A Synchronizer that updates city council districts for lots."""

    def sync(self, data_source):
        logger.info('Starting to synchronize city council districts.')
        self.update_city_council_districts(count=data_source.batch_size or 1000)
        logger.info('Finished synchronizing city council districts.')

    def update_city_council_districts(self, count=1000):
        lots = Lot.objects.filter(
            city_council_district__isnull=True
        ).order_by('?')
        for lot in lots[:count]:
            try:
                lot.city_council_district = Boundary.objects.get(
                    geometry__contains=lot.centroid,
                    layer__name='City Council Districts',
                )
                lot.save()
            except Exception:
                logger.warn('Caught exception while updating zoning for lot '
                            '%s' % lot)
