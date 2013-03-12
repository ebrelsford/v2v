from django.db import models
from django.utils.translation import ugettext_lazy as _

from inplace.models import Place

from phillydata.availableproperties.models import AvailableProperty
from phillydata.opa.models import BillingAccount
from phillydata.owners.models import Owner
from phillydata.parcels.models import Parcel
from phillydata.violations.models import Violation
from phillydata.waterdept.models import WaterParcel


class Lot(Place):

    owner = models.ForeignKey(Owner,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('The owner of this lot.'),
        verbose_name=_('owner'),
    )
    billing_account = models.ForeignKey(BillingAccount,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_("The owner's billing account for this lot."),
        verbose_name=_('billing account'),
    )
    parcel = models.ForeignKey(Parcel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('The parcel this lot is based on.'),
        verbose_name=_('parcel'),
    )
    violations = models.ManyToManyField(Violation,
        blank=True,
        null=True,
        help_text=_('The violations associated with this lot.'),
        verbose_name=_('violations'),
    )
    available_property = models.ForeignKey(AvailableProperty,
        blank=True,
        null=True,
    )
    water_parcel = models.ForeignKey(WaterParcel,
        blank=True,
        null=True,
        help_text=_('The parcel the Water Department defines for this lot')
    )

    added = models.DateTimeField(_('date added'),
        auto_now_add=True,
        help_text=('When this lot was added'),
    )

    # TODO
    # land use
    # tax delinquency (private)
    # zoning

    def __unicode__(self):
        return u'Lot (%s)' % (self.address_line1,)
