import logging

import external_data_sync
from external_data_sync.synchronizers import Synchronizer
from lots.models import Lot

from .adapter import find_water_dept_details


logger = logging.getLogger(__name__)


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


external_data_sync.register(WaterDeptSynchronizer)
