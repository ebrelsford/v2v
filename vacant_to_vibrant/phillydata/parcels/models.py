from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class Parcel(models.Model):
    """
    A parcel as defined by the Department of Records.

    More information here:
        http://opendataphilly.org/opendata/resource/28/property-parcels/

    """
    objects = models.GeoManager()

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
