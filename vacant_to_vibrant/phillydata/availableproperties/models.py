from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

import reversion

from vacant_to_vibrant.reversion_utils import InitialRevisionManagerMixin


class AvailablePropertyManager(InitialRevisionManagerMixin, models.GeoManager):
    pass


class AvailableProperty(models.Model):
    """
    An available property as designated by the Philadelphia Redevelopment
    Authority.

    """
    objects = AvailablePropertyManager()
    centroid = models.PointField(_('centroid'))

    #
    # Data from the Available Property API
    #
    asset_id = models.CharField(_('asset id'),
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        help_text=_('The asset ID'),
    )
    mapreg = models.CharField(_('mapreg'),
        max_length=10,
        blank=True,
        null=True,
        help_text=_("The parcel's registry number"),
    )
    address = models.CharField(_('address'),
        max_length=200,
        blank=True,
        null=True,
        help_text=_("The parcel's address"),
    )
    description = models.TextField(_('description'),
        blank=True,
        null=True,
    )
    agency = models.CharField(_('agency'),
        max_length=20,
        blank=True,
        null=True,
        help_text=_('The agency that holds this parcel'),
    )
    price = models.DecimalField(_('price'),
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('The price of this property'),
    )
    price_str = models.CharField(_('price string'),
        max_length=50,
        blank=True,
        null=True,
        help_text=_('The price string for this property--does not always match '
                    'the numeric price'),
    )
    area = models.DecimalField(_('area'),
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('The area of this property in square feet'),
    )

    #
    # Meta
    #
    STATUS_NEW = 'new and available'
    STATUS_AVAILABLE = 'available'
    STATUS_CHOICES = (
        (STATUS_NEW, STATUS_NEW),
        (STATUS_AVAILABLE, STATUS_AVAILABLE),
        ('no longer available', 'no longer available'),
    )
    status = models.CharField(_('status'),
        choices=STATUS_CHOICES,
        default='new and available',
        max_length=30,
    )
    added = models.DateTimeField(_('date added'),
        auto_now_add=True,
        help_text=('The first time this property was seen in the available '
                   'propery list'),
    )
    last_seen = models.DateTimeField(_('date last seen'),
        help_text=('The last time this property was seen in the available '
                   'propery list'),
    )

    def __unicode__(self):
        return '%s, asset id: %s, %s' % (self.address, self.asset_id, self.status)

    class Meta:
        verbose_name = _('available property')
        verbose_name_plural = _('available properties')

reversion.register(AvailableProperty)
