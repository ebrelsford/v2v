import logging

import external_data_sync
from external_data_sync.synchronizers import Synchronizer
from inplace.boundaries.models import Boundary
from lots.models import Lot


logger = logging.getLogger(__name__)


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


external_data_sync.register(CityCouncilSynchronizer)
