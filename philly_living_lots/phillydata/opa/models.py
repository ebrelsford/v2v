from django.db import models
from django.utils.translation import ugettext_lazy as _

import reversion


class AccountOwner(models.Model):

    name = models.CharField(_('name'),
        max_length=256,
        unique=True,
    )
    owner = models.ForeignKey('owners.Owner',
        verbose_name=_('owner'),
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'%s' % (self.name,)


class BillingAccount(models.Model):

    account_owner = models.ForeignKey('AccountOwner',
        verbose_name=_('account owner'),
        blank=True,
        null=True,
    )
    external_id = models.CharField(_('external id'),
        max_length=50,
        help_text=_('The OPA account number'),
        unique=True,
    )
    property_address = models.CharField(_('property address'),
        max_length=300,
        blank=True,
        null=True,
        help_text=_('The address of the property this account is associated with'),
    )

    improvement_description = models.CharField(_('improvement description'),
        max_length=300,
        blank=True,
        null=True,
        help_text=_('The improvement description according to OPA'),
    )
    sale_date = models.DateField(_('sale date'),
        blank=True,
        null=True,
        help_text=_('The date of the last sale of this property according to '
                    'the OPA'),
    )

    land_area = models.DecimalField(_('land area (sq ft)'),
        max_digits=20,
        decimal_places=3,
        blank=True,
        null=True,
        help_text=_('The land area of the property according to the OPA in '
                    'square feet'),
    )
    improvement_area = models.IntegerField(_('improvement area'),
        blank=True,
        null=True,
        help_text=_('The improvement area of the property according to the OPA'),
    )
    assessment = models.DecimalField(_('assessment'),
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('The assessment of the property according to the OPA'),
    )

    mailing_name = models.CharField(_('mailing name'),
        max_length=300,
        blank=True,
        null=True,
        help_text=_('The name on the mailing address for this account.'),
    )
    mailing_address = models.CharField(_('mailing address'),
        max_length=300,
        blank=True,
        null=True,
        help_text=_('The mailing address for this account.'),
    )
    mailing_postal_code = models.CharField(_('mailing postal code'),
        max_length = 10,
        blank=True,
        null=True,
    )
    mailing_city = models.CharField(_('mailing city'),
        max_length=50,
        blank=True,
        null=True,
    )
    mailing_state_province = models.CharField(_('mailing state/province'),
        max_length=40,
        blank=True,
        null=True,
    )
    mailing_country = models.CharField(_('mailing country'),
        max_length=40,
        blank=True,
        null=True,
        default='USA',
    )

    # TODO periodically update this information
    last_updated = models.DateTimeField(_('last updated'), auto_now=True)

    def __unicode__(self):
        return u'%s: %s, %s, %s, %s' % (
            self.external_id, self.mailing_name, self.mailing_address,
            self.mailing_city, self.mailing_state_province,)

reversion.register(BillingAccount)
