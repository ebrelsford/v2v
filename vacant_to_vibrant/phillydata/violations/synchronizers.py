import logging

import external_data_sync
from external_data_sync.synchronizers import Synchronizer
from lots.load import load_lots_with_violations

from .adapter import find_violations


logger = logging.getLogger(__name__)


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


external_data_sync.register(LIViolationsSynchronizer)
