from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class Place(models.Model):
    """A place."""

    objects = models.GeoManager()

    centroid = models.PointField(_('centroid'),
        null=True,
    )
    polygon = models.MultiPolygonField(_('polygon'),
        null=True,
        blank=True,
    )

    name = models.CharField(_('name'),
        max_length=256,
        null=True,
        blank=True,
    )

    address_line1 = models.CharField(_('address line 1'),
        max_length=150,
        blank=True,
        null=True,
    )
    address_line2 = models.CharField(_('address line 2'),
        max_length=150,
        blank=True,
        null=True,
    )
    postal_code = models.CharField(_('postal code'),
        max_length = 10,
        blank=True,
        null=True,
    )
    city = models.CharField(_('city'),
        max_length=50,
        blank=True,
        null=True,
    )
    state_province = models.CharField(_('state/province'),
        max_length=40,
        blank=True,
        null=True,
    )
    country = models.CharField(_('country'),
        max_length=40,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    @classmethod
    def _app_and_object(cls):
        meta = cls._meta
        return (meta.app_label.lower(), meta.object_name.lower())

    @models.permalink
    def get_absolute_url(self):
        return ('places:%s_%s_detail' % self._app_and_object(), (), {
            'pk': self.pk,
        })

    @models.permalink
    def get_geojson_url(self):
        return ('places:%s_%s_detail_geojson' % self._app_and_object(), (), {
            'pk': self.pk,
        })

    @models.permalink
    def get_popup_url(self):
        return ('places:%s_%s_detail_popup' % self._app_and_object(), (), {
            'pk': self.pk,
        })

    @classmethod
    def get_list_geojson_url(cls):
        from django.core.urlresolvers import reverse
        return reverse('places:%s_%s_geojson' % cls._app_and_object())
