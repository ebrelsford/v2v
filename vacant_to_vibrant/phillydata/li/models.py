from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class Location(models.Model):
    """
    A location in the L&I database.

    """
    objects = models.GeoManager()

    point = models.PointField(_('point'))
    address = models.CharField(_('address'),
        max_length=300,
        blank=True,
        null=True,
        help_text=_('The street address, created by concatenating house '
                    'number and street fields.'),
    )
    zip_code = models.CharField(_('zip code'),
        max_length=20,
        blank=True,
        null=True,
    )
    external_id = models.CharField(_('external ID'),
        max_length=30,
        help_text=_("The ID of this location in L&I's API"),
        unique=True,
    )

    def __unicode__(self):
        return u'(%s): %s, %s' % (self.external_id, self.address, self.zip_code)
