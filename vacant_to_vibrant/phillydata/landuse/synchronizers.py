import logging

import external_data_sync
from external_data_sync.synchronizers import Synchronizer
from lots.load import load_lots_land_use_vacant

from .adapter import find_land_use_areas


logger = logging.getLogger(__name__)


class LandUseAreaSynchronizer(Synchronizer):
    """Synchronizes LandUseAreas."""

    def sync(self, data_source):
        logger.info('Synchronizing vacant land use area data.')
        find_land_use_areas()
        logger.info('Done synchronizing vacant land use area data.')

        logger.info('Adding lots with vacant land use areas.')
        load_lots_land_use_vacant(added_after=data_source.last_synchronized)
        logger.info('Done adding lots with vacant land use areas.')


external_data_sync.register(LandUseAreaSynchronizer)
