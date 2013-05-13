from django.contrib.contenttypes.generic import GenericRelation
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.measure import D
from django.db import models
from django.utils.translation import ugettext_lazy as _

from inplace.models import Place, PlaceManager

from organize.models import Organizer, Watcher
from phillydata.availableproperties.models import AvailableProperty
from phillydata.landuse.models import LandUseArea
from phillydata.opa.models import BillingAccount
from phillydata.owners.models import Owner
from phillydata.parcels.models import Parcel
from phillydata.taxaccounts.models import TaxAccount
from phillydata.violations.models import Violation
from phillydata.waterdept.models import WaterParcel
from vacant_to_vibrant.reversion_utils import InitialRevisionManagerMixin


class LotManager(InitialRevisionManagerMixin, PlaceManager):

    def find_nearby(self, lot):
        """Find lots near the given lot."""
        return self.get_query_set().filter(
            centroid__distance_lte=(lot.centroid, D(mi=.5))
        )


class Lot(Place):

    objects = LotManager()

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
    licenses = models.ManyToManyField('licenses.License',
        blank=True,
        null=True,
        help_text=_('The licenses associated with this lot.'),
        verbose_name=_('licenses'),
    )
    available_property = models.ForeignKey(AvailableProperty,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    water_parcel = models.ForeignKey(WaterParcel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('The parcel the Water Department defines for this lot')
    )
    known_use = models.ForeignKey('Use',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    known_use_certainty = models.PositiveIntegerField(_('known use certainty'),
        default=0,
        help_text=_('On a scale of 0 to 10, how certain are we that the known '
                    'use is correct?'),
    )
    known_use_locked = models.BooleanField(_('known use locked'),
        default=False,
        help_text=_('Is the known use field locked? If it is not, the site '
                    'will make a guess using available data. If you are '
                    'certain that the known use is correct, lock it.'),
    )
    zoning_district = models.ForeignKey('zoning.BaseDistrict',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('zoning district'),
    )
    city_council_district = models.ForeignKey('boundaries.Boundary',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('city council district'),
    )

    added = models.DateTimeField(_('date added'),
        auto_now_add=True,
        help_text=('When this lot was added'),
    )

    organizers = GenericRelation(Organizer)
    watchers = GenericRelation(Watcher)

    group = models.ForeignKey('LotGroup',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('group'),
    )

    polygon_area = models.DecimalField(_('polygon area'),
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('The area of the polygon in square feet'),
    )
    polygon_width = models.DecimalField(_('polygon width'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('The width of the polygon in feet'),
    )

    class Meta:
        permissions = (
            ('view_all_details', 'Can view all details for lots'),
            ('view_all_filters', 'Can view all map filters for lots'),
        )

    def __unicode__(self):
        return u'%s' % (self.address_line1,)

    @models.permalink
    def get_absolute_url(self):
        return ('lots:lot_detail', (), { 'pk': self.pk, })

    def find_nearby(self, count=5):
        return self.objects.find_nearby(self)[:count]

    def calculate_polygon_area(self):
        """Find the area of this lot in square feet using its polygon."""
        try:
            # tranform to an area-preserving projection for south PA
            return self.polygon.transform(102729, clone=True).area
        except Exception:
            return None

    def _get_area(self):
        if self.billing_account:
            return self.billing_account.land_area
        if self.water_parcel:
            return self.water_parcel.gross_area
        return self.calculate_polygon_area()
    area = property(_get_area)

    def _get_number_of_lots(self):
        return 1
    number_of_lots = property(_get_number_of_lots)

    def _get_nearby_lots(self):
        nearby = Lot.objects.filter(
            centroid__distance_lte=(self.centroid, D(mi=.1))
        )
        nearby = nearby.exclude(pk=self.pk)
        nearby = nearby.distance(self.centroid).order_by('distance')
        return nearby[:5]
    nearby = property(_get_nearby_lots)

    def _get_latitude(self):
        try:
            return self.centroid.y
        except Exception:
            return None
    latitude = property(_get_latitude)

    def _get_longitude(self):
        try:
            return self.centroid.x
        except Exception:
            return None
    longitude = property(_get_longitude)


class LotGroup(Lot):
    """A group of lots."""

    def add(self, lot):
        """Add a lot to this group."""
        lots = set(list(self.lot_set.all()))
        lots.add(lot)
        self.update(lots=lots)

    def remove(self, lot):
        """Remove a lot from this group."""
        lots = list(self.lot_set.all())
        lots.remove(lot)
        self.update(lots=lots)

    def update(self, lots=None):
        """
        Update this group with the given lots. Allow lots to be passed
        manually since this might be called on a lot's pre_save signal.
        """

        if not lots:
            lots = self.lot_set.all()

        # Update polygon
        self.polygon = None
        for lot in lots:
            if not lot.polygon: continue
            if not self.polygon:
                self.polygon = lot.polygon
            else:
                union = self.polygon.union(lot.polygon)
                if not isinstance(union, MultiPolygon):
                    union = MultiPolygon([union])
                self.polygon = union

        # Update centroid
        self.centroid = self.polygon.centroid

        # Could update other things here, but maybe we should just proxy them
        # on the fly?

        self.save()

    def __unicode__(self):
        return self.name

    def _get_number_of_lots(self):
        return sum([l.number_of_lots for l in self.lot_set.all()])
    number_of_lots = property(_get_number_of_lots)


class Use(models.Model):
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=200)

    def __unicode__(self):
        return self.name


from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Lot)
def save_lot_update_group(sender, instance=None, **kwargs):
    """Update the group that this member is part of."""
    if not instance: return

    # Try to get the group this instance was part of, if any
    try:
        previous_group = Lot.objects.get(pk=instance.pk).group
    except Exception:
        previous_group = None

    # Get the group this instance will be part of, if any
    next_group = instance.group

    # If instance was in a group before but no longer will be, update that
    # group accordingly
    if previous_group and previous_group != next_group:
        previous_group.remove(instance)

    # If instance was not in a group before but will be, update that group
    if next_group and next_group != previous_group:
        next_group.add(instance)


@receiver(post_delete, sender=Lot)
def delete_lot_update_group(sender, instance=None, **kwargs):
    if instance.group:
        instance.group.update()
