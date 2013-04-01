from django.db import models
from django.utils.translation import ugettext_lazy as _

from vacant_to_vibrant.reversion_utils import InitialRevisionManagerMixin


class WaterParcelManager(InitialRevisionManagerMixin, models.Manager):
    pass


class WaterParcel(models.Model):
    """
    A parcel defined by the Philadelphia Water Department.

    May not be strictly the same as parcels as defined by Records.

    """

    objects = WaterParcelManager()

    # TODO shape?
    #"Shape": "POLYGON ((2703814.74156681 254477.754747897, 2703813.02798755 254463.902413398, 2703743.47825789 254472.777067557, 2703745.30371356 254486.647118554, 2703814.74156681 254477.754747897))",

    # IDs
    parcel_id = models.CharField(_('parcel id'),
        max_length=20,
        blank=True,
        null=True,
        help_text=_('The parcel ID assigned by the Water Dept'),
    )
    brt_account = models.CharField(_('BRT account'),
        max_length=20,
        blank=True,
        null=True,
        help_text=_('The OPA/BRT account according to the Water Dept'),
    )
    ten_code = models.CharField(_('ten code'),
        max_length=20,
        blank=True,
        null=True,
    )

    # parcel information
    owner1 = models.CharField(_('owner1'),
        max_length=256,
        blank=True,
        null=True,
    )
    owner2 = models.CharField(_('owner1'),
        max_length=256,
        blank=True,
        null=True,
    )
    address = models.CharField(_('address'),
        max_length=256,
        blank=True,
        null=True,
    )

    gross_area = models.DecimalField(_('gross area'),
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('The area of the parcel in square feet')
    )
    # TODO if this is very low parcel may be vacant
    impervious_area = models.DecimalField(_('impervious area'),
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('The impervious area of the parcel in square feet')
    )

    # building information
    # TODO these fields will have hints to vacancy--eg,
    # 'building_description' startswith 'VAC LAND'
    building_type = models.CharField(_('building type'),
        max_length=50,
        blank=True,
        null=True,
    )
    building_description = models.CharField(_('building description'),
        max_length=100,
        blank=True,
        null=True,
    )
    building_code = models.CharField(_('building code'),
        max_length=20,
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return '%s at %s, owned by %s, %s' % (self.parcel_id, self.address,
                                              self.owner1, self.owner2 or '')


class WaterAccount(models.Model):
    """An account with the Philadelphia Water Department."""
    water_parcel = models.ForeignKey('WaterParcel',
        verbose_name=_('water parcel')
    )

    account_id = models.CharField(_('account ID'),
        max_length=30,
        blank=True,
        null=True,
        help_text=_('The ID of this account with the Water Department'),
    )
    account_number = models.CharField(_('account number'),
        max_length=30,
        blank=True,
        null=True,
        help_text=_('A slightly expanded version of the account ID'),
    )
    customer_id = models.CharField(_('customer ID'),
        max_length=20,
        blank=True,
        null=True,
        help_text=_('The ID for this customer with the Water Department'),
    )
    customer_name = models.CharField(_('customer name'),
        max_length=100,
        blank=True,
        null=True,
    )
    inst_id = models.CharField(_('inst ID'),
        max_length=20,
        blank=True,
        null=True,
    )

    # TODO 'Discontinued' could indicate vacancy
    account_status = models.CharField(_('account status'),
        max_length=30,
        blank=True,
        null=True,
        help_text=_('Discontinued / Current'),
    )
    account_status_abbreviation = models.CharField(_('account status abbreviation'),
        max_length=10,
        blank=True,
        null=True,
    )

    meter_size = models.CharField(_('meter size'),
        max_length=30,
        blank=True,
        null=True,
    )
    meter_size_abbreviation = models.CharField(_('meter size abbreviation'),
        max_length=10,
        blank=True,
        null=True,
    )

    service_type = models.CharField(_('service type'),
        max_length=10,
        blank=True,
        null=True,
    )
    # TODO '3 - Stormwater Only' might indicate vacancy
    service_type_label = models.CharField(_('service type label'),
        max_length=50,
        blank=True,
        null=True,
    )

    stormwater_status = models.CharField(_('stormwater status'),
        max_length=30,
        blank=True,
        null=True,
        help_text=_('Billed / Not Billed'),
    )

    def __unicode__(self):
        return '%s (%s), %s' % (self.account_id, self.account_status,
                                self.service_type_label)
