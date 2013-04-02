import logging

from django.contrib.gis.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger(__name__)


class ParcelManager(models.GeoManager):

    def _debug_too_many_parcels(self, parcels):
        if not logger.isEnabledFor(logging.DEBUG): return
        count = parcels.count()
        if count > 5:
            parcels = parcels[:5]
        parcel_strs = [str(parcel) for parcel in parcels]
        logger.debug('Too many parcels (%d): %s' %
                     (count, '\n * '.join(parcel_strs)))


    def get_fuzzy(self, address=None, centroid=None, mapreg=None):
        """Attempt to get a Parcel using the given parameters."""
        filters = Q()

        if not address and not centroid and not mapreg:
            raise self.model.DoesNotExist('Parcel matching query could not be '
                                          'found--no filters given. Be more '
                                          'specific!')

        # Try optimistic, fast query--assumes everything present will match
        if centroid:
            filters = filters & Q(geometry__contains=centroid)
        if address:
            filters = filters & (Q(address__iexact=address) |
                                 Q(address__icontains=address))
        if mapreg:
            filters = filters & Q(mapreg=mapreg)

        logger.debug('Trying optimistic search. Filters: %s' % str(filters))
        parcels = self.filter(filters)
        if parcels.count() == 1:
            return parcels[0]

        # Optimistic failed, try each filter individually
        parcels = self.all()
        if address:
            logger.debug('Trying to filter by address: "%s"' % address)
            parcels = parcels.filter(address__iexact=address)
            if parcels.count() == 1:
                return parcels[0]
            if parcels.count() > 1:
                logger.debug('Found too many parcels for address "%s"' %
                             address)
                self._debug_too_many_parcels(parcels)
            else:
                parcels = self.all()

            logger.debug('Trying to filter more loosely by address: "%s"' %
                         address)
            parcels = parcels.filter(address__icontains=address)
            count = parcels.count()
            if count == 1:
                return parcels[0]
            if count > 1:
                logger.debug(('Found too many parcels while searching loosely '
                              'for address %s') % address)
                self._debug_too_many_parcels(parcels)

        # filter by mapreg
        if mapreg:
            logger.debug('Trying to filter by mapreg: "%s"' % mapreg)
            parcels = parcels.filter(mapreg=mapreg)
            count = parcels.count()
            if count == 1:
                return parcels[0]
            if count > 1:
                logger.debug('Found too many parcels for mapreg %s' % mapreg)
                self._debug_too_many_parcels(parcels)
            else:
                parcels = self.all()

        # filter by centroid
        if centroid:
            logger.debug('Trying to filter by centroid: "%s"' % str(centroid))
            parcels = parcels.filter(geometry__contains=centroid)
            count = parcels.count()
            if count == 1:
                return parcels[0]
            if count > 1:
                # TODO something to choose a parcel--compare distance from
                # target centroid (and maybe area--make 'polygon' a parameter?)
                logger.debug('Found too many parcels for centroid %s' %
                             str(centroid))
                self._debug_too_many_parcels(parcels)
            else:
                parcels = self.all()

        if parcels.count() > 1:
            self._debug_too_many_parcels(parcels)
            raise self.model.MultipleObjectsReturned(
                ('Parcel matching query could not be found. There were %d '
                 'potential matches.' % parcels.count())
            )

        raise self.model.DoesNotExist('Parcel matching query could not be '
                                      'found.')


class Parcel(models.Model):
    """
    A parcel as defined by the Department of Records.

    More information here:
        http://opendataphilly.org/opendata/resource/28/property-parcels/

    """
    #objects = models.GeoManager()
    objects = ParcelManager()

    geometry = models.MultiPolygonField(_('geometry'))

    basereg = models.CharField(_('basereg'),
        max_length=10,
        blank=True,
        null=True,
        help_text=_('The registry number which there is a deed attached to.')
    )

    mapreg = models.CharField(_('mapreg'),
        max_length=10,
        blank=True,
        null=True,
        help_text=_('A registry number that may or may not specifically have '
                    'a deed attached to it.')
    )

    stcod = models.CharField(_('stcod'),
        max_length=10,
        blank=True,
        null=True,
        help_text=_('Street code. Maintained by the Department of Streets.')
    )

    address = models.CharField(_('address'),
        max_length=300,
        blank=True,
        null=True,
        help_text=_('The street address, created by concatenating house '
                    'number and street fields from the parcel database.')
    )

    def __unicode__(self):
        return u'Parcel (%s)' % (self.address,)
