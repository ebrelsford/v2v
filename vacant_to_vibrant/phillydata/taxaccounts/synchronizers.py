import logging

import external_data_sync
from external_data_sync.synchronizers import Synchronizer
from lots.models import Lot

from .models import TaxAccount


logger = logging.getLogger(__name__)


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


external_data_sync.register(TaxAccountSynchronizer)
