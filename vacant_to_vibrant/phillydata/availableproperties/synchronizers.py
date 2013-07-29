import logging

import external_data_sync
from external_data_sync.synchronizers import Synchronizer
from lots.load import load_lots_available

from .adapter import (find_available_properties,
                      find_no_longer_available_properties)


logger = logging.getLogger(__name__)


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


external_data_sync.register(PRAAvailablePropertiesSynchronizer)
