from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from vacant_to_vibrant.reversion_utils import InitialRevisionManagerMixin


class LandUseAreaManager(InitialRevisionManagerMixin, models.GeoManager):
    pass


class LandUseArea(models.Model):
    """
    A land use area as defined by the Philadelphia City Planning Commission.

    More here:
        http://gis.phila.gov/ArcGIS/rest/services/PhilaOIT-GIS_Boundaries/MapServer/11

    """

    objects = LandUseAreaManager()

    geometry = models.MultiPolygonField(_('geometry'))

    object_id = models.CharField(_('object ID'),
        max_length=15,
        unique=True,
        help_text=_('The object ID (OBJECTID)')
    )

    category = models.CharField(_('category'),
        max_length=30,
        blank=True,
        null=True,
        help_text=_('The land use category (C_DIG1DESC)')
    )

    subcategory = models.CharField(_('subcategory'),
        max_length=30,
        blank=True,
        null=True,
        help_text=_('The land use subcategory (C_DIG2DESC)')
    )

    description = models.CharField(_('description'),
        max_length=30,
        blank=True,
        null=True,
        help_text=_('The land use description (C_DIG3DESC)')
    )

    vacant_building = models.CharField(_('vacant building'),
        max_length=10,
        blank=True,
        null=True,
        help_text=_('(VACBLDG)')
    )

    area = models.DecimalField(_('area'),
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('The area of this parcel in square feet'),
    )

    added = models.DateTimeField(_('date added'),
        auto_now_add=True,
        help_text=('The first time this area was seen in the data source'),
    )

    def __unicode__(self):
        return str(self.object_id)
