from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class BaseDistrict(models.Model):
    """A base area that is all one zoning type."""

    objects = models.GeoManager()

    geometry = models.MultiPolygonField(_('geometry'))
    zoning_type = models.ForeignKey(
        'ZoningType',
        verbose_name=_('zoning type')
    )

    def __unicode__(self):
        return "%d, %s" % (self.pk, self.zoning_type.code)


class ZoningType(models.Model):
    """A type of zoning, added dynamically using the city's zoning maps."""

    objects = models.GeoManager()

    code = models.CharField(_('code'), max_length=30)
    long_code = models.CharField(_('long code'), max_length=30)
    group = models.CharField(_('group'), max_length=100)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        ordering = ('code',)

    def __unicode__(self):
        return self.code
