import logging

import external_data_sync
from external_data_sync.synchronizers import Synchronizer
from lots.models import Lot

from .adapter import find_opa_details

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


external_data_sync.register(OPASynchronizer)
