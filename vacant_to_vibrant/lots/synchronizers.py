import logging

from django.db.models import Q

import external_data_sync
from external_data_sync.synchronizers import Synchronizer
from inplace.boundaries.models import Boundary
from phillydata.opa.adapter import find_opa_details
from phillydata.taxaccounts.models import TaxAccount
from phillydata.waterdept.adapter import find_water_dept_details
from phillydata.zoning.models import BaseDistrict

from .load import (load_lots_available, load_lots_land_use_vacant,
                   load_lots_with_licenses, load_lots_with_violations)
from .models import Lot


logger = logging.getLogger(__name__)


class LotOwnershipSynchronizer(Synchronizer):
    """
    A Synchronizer that updates ownership data for lots using the OPA API.

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
            self.update_lot_owner_data(lot)

    def update_lot_owner_data(self, lot):
        logger.debug('Updating OPA data for lot %s' % lot)
        try:
            kwargs = {}
            if lot.water_parcel:
                kwargs['brt_account'] = lot.water_parcel.brt_account
            lot.billing_account = find_opa_details(lot.address_line1, **kwargs)
            lot.owner = lot.billing_account.account_owner.owner
            lot.save()
        except Exception:
            logger.warn('Caught exception while getting OPA data for lot %s' %
                        lot)


class TaxAccountSynchronizer(Synchronizer):
    """A Synchronizer that updates tax account data for lots."""

    def sync(self, data_source):
        logger.info('Starting to synchronize tax account data.')
        self.update_tax_accounts(count=data_source.batch_size)
        logger.info('Finished synchronizing tax account data.')

    def update_tax_accounts(self, count=1000):
        lots = Lot.objects.filter(tax_account__isnull=True).order_by('?')
        for lot in lots[:count]:
            try:
                lot.tax_account = TaxAccount.objects.get(
                    property_address__icontains=lot.address_line1,
                )
                lot.save()
            except TaxAccount.DoesNotExist:
                logger.debug('Could not find tax account for lot %s' % lot)
            except Exception:
                logger.warn('Caught exception while getting tax account for '
                            'lot %s' % lot)


class LotsAvailablePropertiesSynchronizer(Synchronizer):
    """Load lots for available properties that are new."""

    def sync(self, data_source):
        logger.info('Adding lots with available properties.')
        load_lots_available(added_after=data_source.last_synchronized)
        logger.info('Done adding lots with available properties.')


class LotsLandUseAreaSynchronizer(Synchronizer):
    """Synchronizes Lots with vacant land use areas."""

    def sync(self, data_source):
        logger.info('Adding lots with vacant land use areas.')
        load_lots_land_use_vacant(added_after=data_source.last_synchronized)
        logger.info('Done adding lots with vacant land use areas.')


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


class WaterDeptSynchronizer(Synchronizer):
    """
    A Synchronizer that updates Water Department data.

    """
    def sync(self, data_source):
        logger.info('Starting to synchronize Water Department data.')
        self.update_water_dept_data(count=data_source.batch_size)
        logger.info('Finished synchronizing Water Department data.')

    def update_water_dept_data(self, count=1000):
        # TODO also lots where the water dept data has not been touched in a
        # while
        # Find lots with no water parcel or where the building_description is
        # null
        lots = Lot.objects.filter(
            Q(water_parcel__isnull=True) |
            Q(water_parcel__building_description__isnull=True)
        ).order_by('?')
        for lot in lots[:count]:
            logger.debug('Updating Water Department data for lot %s' % lot)
            try:
                lot.water_parcel = find_water_dept_details(
                    *lot.polygon.centroid.coords
                )
                lot.save()
            except Exception:
                logger.warn('Exception while updating Water Department data '
                            'for lot %s' % lot)


class LotsLILicensesSynchronizer(Synchronizer):
    """Synchronize lots with L&I licenses"""

    def sync(self, data_source):
        logger.info('Adding lots with licenses.')
        load_lots_with_licenses()
        logger.info('Done adding lots with licenses.')


class LotsLIViolationsSynchronizer(Synchronizer):
    """Synchronize lots with L&I violations"""

    def sync(self, data_source):
        logger.info('Adding lots with violations.')
        load_lots_with_violations()
        logger.info('Done adding lots with violations.')


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
                logger.warn('Caught exception while updating city council '
                            'district for lot %s' % lot)


class PlanningDistrictSynchronizer(Synchronizer):
    """A Synchronizer that updates planning districts for lots."""

    def sync(self, data_source):
        logger.info('Starting to synchronize planning districts.')
        self.update_planning_districts(count=data_source.batch_size or 1000)
        logger.info('Finished synchronizing planning districts.')

    def update_planning_districts(self, count=1000):
        lots = Lot.objects.filter(
            planning_district__isnull=True
        ).order_by('?')
        for lot in lots[:count]:
            try:
                lot.planning_district = Boundary.objects.get(
                    geometry__contains=lot.centroid,
                    layer__name='Planning Districts',
                )
                lot.save()
            except Exception:
                logger.warn('Caught exception while updating planning '
                            'district for lot %s' % lot)


class UseCertaintyScoresSynchronizer(Synchronizer):
    """A Synchronizer that updates use certainty scores for lots."""

    def sync(self, data_source):
        logger.info('Starting to synchronize use certainty scores.')
        self.update_use_certainty_scores(count=data_source.batch_size)
        logger.info('Finished synchronizing use certainty scores.')

    def update_use_certainty_scores(self, count=1000):
        # Get lots that look like they haven't been updated and that we can
        # change
        lots = Lot.objects.filter(
            known_use_locked=False,
            known_use_certainty=0
        ).order_by('?')
        for lot in lots[:count]:
            try:
                lot.known_use_certainty = lot.calculate_known_use_certainty()
                lot.save()
            except Exception:
                logger.warn('Caught exception while updating use certainty '
                            'score for lot %s' % lot)


external_data_sync.register(LotOwnershipSynchronizer)
external_data_sync.register(TaxAccountSynchronizer)
external_data_sync.register(LotsAvailablePropertiesSynchronizer)
external_data_sync.register(LotsLandUseAreaSynchronizer)
external_data_sync.register(ZoningSynchronizer)
external_data_sync.register(WaterDeptSynchronizer)
external_data_sync.register(LotsLILicensesSynchronizer)
external_data_sync.register(LotsLIViolationsSynchronizer)
external_data_sync.register(CityCouncilSynchronizer)
external_data_sync.register(PlanningDistrictSynchronizer)
external_data_sync.register(UseCertaintyScoresSynchronizer)
