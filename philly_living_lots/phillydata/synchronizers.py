import logging
import traceback
from urllib2 import URLError

from django.core.exceptions import MultipleObjectsReturned

import reversion

from lots.load import load_lots_available, load_lots_with_violations
from lots.models import Lot
from sync.synchronizers import Synchronizer
from .availableproperties.models import AvailableProperty
from .availableproperties.reader import AvailablePropertyReader
from .opa.adapter import find_opa_details
from .violations.adapter import find_violations
from .waterdept.adapter import find_water_dept_details


logger = logging.getLogger(__name__)


class OPASynchronizer(Synchronizer):
    """
    A Synchronizer that updates ownership data using the OPA API.

    """
    def sync(self, data_source):
        logger.info('Starting to synchronize OPA data.')
        self.update_owner_data()
        logger.info('Finished synchronizing OPA data.')

    def update_owner_data(self):
        # TODO also lots where the owner has not been touched in a while?
        # eg, last_seen for BillingAccount?
        for lot in Lot.objects.filter(owner__isnull=True):
            try:
                lot.billing_account = find_opa_details(lot.address_line1)
                lot.owner = lot.billing_account.account_owner.owner
                lot.save()
            except Exception:
                logger.exception('Caught exception while getting OPA data for '
                                 'lot %s' % lot)


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
        print 'Synchronizing data for Available Properties'

        # update currently available properties
        try:
            reader = AvailablePropertyReader()
            for feature in reader:
                self.create_or_update(reader, feature)
            print 'Done adding data for current Available Properties'

            # check for AvailableProperty objects that were not seen this time
            no_longer_available = AvailableProperty.objects.filter(
                last_seen__lt=data_source.last_synchronized
            )
            no_longer_available.update(status='no longer available')
            print 'Done updating %d no-longer-available Available Properties' % (
                no_longer_available.count(),
            )
        except URLError:
            print ('Synchronizing Available Properties was interrupted by '
                   'exception')
            traceback.print_stack()
            data_source.healthy = False
            data_source.save()

        # add appropriate lots for newly-added Available Properties
        # TODO or is this its own Synchronizer?
        load_lots_available(added_after=data_source.last_synchronized)

    @reversion.create_revision()
    def create_or_update(self, reader, feature):
        try:
            field_dict = reader.model_defaults(feature)
            model, created = AvailableProperty.objects.get_or_create(
                defaults=field_dict,
                **reader.model_get_kwargs(feature)
            )
            if not created:
                field_dict['status'] = 'available'
                AvailableProperty.objects.filter(pk=model.pk).update(**field_dict)
                model = AvailableProperty.objects.get(pk=model.pk)
        except MultipleObjectsReturned:
            # TODO try to narrow it down?
            print ('Multiple objects found when searching for '
                   'AvailableProperty objects with kwargs:',
                   reader.model_get_kwargs(feature))
        return model


    def sync(self, data_source):
        print 'hi, i am syncing over here'
        # TODO
        # update database
        # then update lots
        pass


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
        logger.info('Done lots with violations.')

    def update_violation_data(self):
        for code in self.codes:
            find_violations(code, self.data_source.last_synchronized)
