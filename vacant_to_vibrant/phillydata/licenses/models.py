from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from vacant_to_vibrant.reversion_utils import InitialRevisionManagerMixin


class LicenseManager(InitialRevisionManagerMixin, models.GeoManager):
    pass


class License(models.Model):
    """A license given by Philadelphia L&I"""
    objects = LicenseManager()
    license_type = models.ForeignKey('LicenseType')
    location = models.ForeignKey('li.Location')
    primary_contact = models.ForeignKey('Contact',
        blank=True,
        null=True,
        help_text=_('The primary contact for this license'),
    )

    issued_datetime = models.DateTimeField(_('issued date/time'),
        blank=True,
        null=True,
        help_text=_("When this license was issued"),
    )
    inactive_datetime = models.DateTimeField(_('inactive date/time'),
        blank=True,
        null=True,
        help_text=_("When this license became inactive, if it is"),
    )
    external_id = models.CharField(_('external ID'),
        max_length=30,
        help_text=_("L&I's license number for this particular license"),
        unique=True,
    )
    expires_month = models.CharField(_('month of expiry'),
        blank=True,
        max_length=30,
        null=True,
        help_text=_('The month this license will expire'),
    )
    expires_year = models.PositiveIntegerField(_('year of expiry'),
        blank=True,
        null=True,
        help_text=_("The year this license will expire"),
    )
    status = models.CharField(_('status'),
        blank=True,
        max_length=30,
        null=True,
        help_text=_('The last-known status of this license'),
    )

    def __unicode__(self):
        return u'%s: %s, %s' % (self.external_id, self.license_type,
                                self.location,)


class LicenseType(models.Model):
    """A type of L&I license"""

    code = models.CharField(_('code'),
        max_length=32,
        help_text=_('The code L&I uses for this type of license.'),
        unique=True,
    )
    name = models.TextField(_('name'),
        help_text=_('The name L&I gives for this type of license.'),
    )

    def __unicode__(self):
        return u'%s: %s' % (self.code, self.name,)


class Contact(models.Model):
    """A contact with respect to an L&I license"""
    contact_type = models.CharField(_('contact type'),
        blank=True,
        max_length=32,
        null=True,
    )
    company_name = models.CharField(_('company name'),
        blank=True,
        max_length=300,
        null=True,
    )
    first_name = models.CharField(_('first name'),
        blank=True,
        max_length=300,
        null=True,
    )
    last_name = models.CharField(_('last name'),
        blank=True,
        max_length=300,
        null=True,
    )
    address1 = models.CharField(_('address1'),
        blank=True,
        max_length=300,
        null=True,
    )
    address2 = models.CharField(_('address2'),
        blank=True,
        max_length=300,
        null=True,
    )
    city = models.CharField(_('city'),
        blank=True,
        max_length=300,
        null=True,
    )
    state = models.CharField(_('state'),
        blank=True,
        max_length=100,
        null=True,
    )
    zip_code = models.CharField(_('zip code'),
        blank=True,
        max_length=20,
        null=True,
    )

    def __unicode__(self):
        try:
            return u'%s %s, %s' % (self.first_name, self.last_name,
                                   self.contact_type,)
        except Exception:
            return '%d' % self.pk
