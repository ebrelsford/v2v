from django.db import models
from django.utils.translation import ugettext_lazy as _

from vacant_to_vibrant.reversion_utils import InitialRevisionManagerMixin


class TaxAccountManager(InitialRevisionManagerMixin, models.Manager):
    pass


class TaxAccount(models.Model):

    objects = TaxAccountManager()

    owner_name = models.CharField(_('owner name'),
        max_length=256,
    )

    owner_name2 = models.CharField(_('owner name #2'),
        max_length=256,
    )

    brt_number = models.CharField(_('BRT number'),
        max_length=10,
        unique=True,
    )

    property_address = models.CharField(_('property address'),
        max_length=300,
        blank=True,
        null=True,
        help_text=_('The property address for this account.'),
    )

    property_city = models.CharField(_('property city'),
        max_length=50,
        blank=True,
        null=True,
    )

    property_state_province = models.CharField(_('property state/province'),
        max_length=40,
        blank=True,
        null=True,
    )

    property_postal_code = models.CharField(_('property postal code'),
        max_length = 10,
        blank=True,
        null=True,
    )

    building_description = models.CharField(_('building description'),
        max_length=100,
        blank=True,
        null=True,
    )

    building_category = models.CharField(_('building category'),
        max_length=100,
        blank=True,
        null=True,
    )

    billing_account = models.ForeignKey('opa.BillingAccount',
        verbose_name=_('billing account'),
        blank=True,
        null=True,
    )

    amount_delinquent = models.DecimalField(_('amount delinquent'),
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('The amount this account is delinquent'),
    )

    years_delinquent = models.IntegerField(_('years delinquent'),
        blank=True,
        null=True,
        help_text=_('Count_of_Years from the delinquency data source'),
    )

    min_period = models.DateField(_('min period'),
        blank=True,
        null=True,
        help_text=_('Min_Period from the delinquency data source, presumably '
                    'when the account entered delinquency'),
    )

    max_period = models.DateField(_('max period'),
        blank=True,
        null=True,
        help_text=_('Max_Period from the delinquency data source, presumably '
                    'when the account left delinquency'),
    )

    taxable_assessment = models.DecimalField(_('taxable assessment'),
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
    )

    exempt_abate_assessment = models.DecimalField(_('exempt abate assessment'),
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
    )

    market_value = models.DecimalField(_('market value'),
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
    )

    last_updated = models.DateField(_('last updated'),
        blank=True,
        null=True,
        help_text=_('The date this data was collected'),
    )

    taxable_assessment = models.DecimalField(_('taxable assessment'),
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
    )

    exempt_abate_assessment = models.DecimalField(_('exempt abate assessment'),
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
    )

    market_value = models.DecimalField(_('market value'),
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
    )

    last_updated = models.DateField(_('last updated'),
        blank=True,
        null=True,
        help_text=_('The date this data was collected'),
    )

    def __unicode__(self):
        return '%s: %s' % (self.brt_number, self.property_address or '',)
