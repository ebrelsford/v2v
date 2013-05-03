from django.db import models
from django.utils.translation import ugettext_lazy as _


class CityCouncilMember(models.Model):

    name = models.CharField(_('name'),
        max_length=256,
    )
    district = models.ForeignKey('boundaries.Boundary',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('district'),
    )
    url = models.URLField(_('url'),
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return self.name
