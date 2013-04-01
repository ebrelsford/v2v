from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from vacant_to_vibrant.reversion_utils import InitialRevisionManagerMixin


class ViolationManager(InitialRevisionManagerMixin, models.GeoManager):
    pass


class Violation(models.Model):
    """
    A violation on a specific parcel.

    """
    objects = ViolationManager()
    violation_type = models.ForeignKey('ViolationType')
    violation_location = models.ForeignKey('ViolationLocation')

    violation_datetime = models.DateTimeField(_('date/time'),
        blank=True,
        null=True,
    )
    external_id = models.CharField(_('external ID'),
        max_length=30,
        help_text=_("The ID of this violation in L&I's API"),
        unique=True,
    )

    # TODO add
    #status

    def __unicode__(self):
        return u'Violation (%s): %s at %s' % (self.external_id,
                                              self.violation_type.li_description,
                                              self.violation_location.address)


class ViolationType(models.Model):
    """
    A type of violation, as defined by the Philadelphia Department of
    Licenses and Inspections.

    """
    code = models.CharField(_('code'),
        max_length=32,
        help_text=_('The code L&I uses for this type of violation.'),
        unique=True,
    )

    li_description = models.TextField(_('L&I description'),
        help_text=_('The description L&I gives for this type of violation.'),
    )

    full_description = models.TextField(_('full description'),
        blank=True,
        null=True,
        help_text=_('A longer description of this type of violation.'),
    )

    def __unicode__(self):
        return u'(%s): %s' % (self.code, self.li_description,)


class ViolationLocation(models.Model):
    """
    Where a violation was recorded.

    """
    objects = models.GeoManager()

    point = models.PointField(_('point'))
    address = models.CharField(_('address'),
        max_length=300,
        blank=True,
        null=True,
        help_text=_('The street address, created by concatenating house '
                    'number and street fields from the violation.'),
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
