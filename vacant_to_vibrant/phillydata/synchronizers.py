import logging

from external_data_sync.synchronizers import Synchronizer
from inplace.boundaries.models import Boundary

from lots.models import Lot


logger = logging.getLogger(__name__)


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
