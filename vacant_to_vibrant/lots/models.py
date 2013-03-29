from django.contrib.contenttypes.generic import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _

from inplace.models import Place

from organize.models import Organizer, Watcher
from phillydata.availableproperties.models import AvailableProperty
from phillydata.landuse.models import LandUseArea
from phillydata.opa.models import BillingAccount
from phillydata.owners.models import Owner
from phillydata.parcels.models import Parcel
from phillydata.taxaccounts.models import TaxAccount
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
    tax_account = models.ForeignKey(TaxAccount,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_("The tax account for this lot."),
        verbose_name=_('tax account'),
    )
    parcel = models.ForeignKey(Parcel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('The parcel this lot is based on.'),
        verbose_name=_('parcel'),
    )
    land_use_area = models.ForeignKey(LandUseArea,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('The land use area for this lot.'),
        verbose_name=_('land use'),
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
    known_use = models.ForeignKey('Use',
        blank=True,
        null=True,
    )

    added = models.DateTimeField(_('date added'),
        auto_now_add=True,
        help_text=('When this lot was added'),
    )

    organizers = GenericRelation(Organizer)
    watchers = GenericRelation(Watcher)

    # TODO
    # zoning

    def __unicode__(self):
        return u'Lot (%s)' % (self.address_line1,)

    @models.permalink
    def get_absolute_url(self):
        return ('lots:lot_detail', (), { 'pk': self.pk, })


class Use(models.Model):
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=200)

    def __unicode__(self):
        return self.name
