from django import forms
from django.utils.translation import ugettext_lazy as _

from chosen.forms import ChosenSelectMultiple
from inplace.boundaries.models import Boundary, Layer

from phillydata.availableproperties.models import AvailableProperty
from phillydata.owners.models import Owner
from phillydata.zoning.models import ZoningType
from .models import Use


class FiltersForm(forms.Form):

    #
    # Hidden filters
    #
    centroid__within = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )
    centroid = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )
    zoom = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )
    limit = forms.CharField(
        initial='1000',
        required=False,
        widget=forms.HiddenInput,
    )
    parents_only = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput,
    )


    #
    # Default filters
    #
    available_property__status__in = forms.MultipleChoiceField(
        choices=AvailableProperty.STATUS_CHOICES,
        initial=(
            AvailableProperty.STATUS_AVAILABLE,
            AvailableProperty.STATUS_NEW,
        ),
        label=_('Available property status'),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )
    polygon_area__gt = forms.IntegerField(
        label=_('Area (sq ft) greater than'),
        required=False,
    )
    polygon_area__lt = forms.IntegerField(
        label=_('Area (sq ft) less than'),
        required=False,
    )
    polygon_width__gt = forms.IntegerField(
        label=_('Width (ft) greater than'),
        required=False,
    )
    polygon_width__lt = forms.IntegerField(
        label=_('Width (ft) less than'),
        required=False,
    )
    known_use_certainty__gt = forms.IntegerField(
        initial=3,
        label=_('Known use certainty greater than'),
        required=False,
    )
    known_use_certainty__lt = forms.IntegerField(
        initial=11,
        label=_('Known use certainty less than'),
        required=False,
    )


    #
    # View types
    #
    view_type = forms.ChoiceField(
        choices=(
            ('tiles', _('points view')),
            ('choropleth', _('summary view')),
        ),
        initial='tiles',
        label=_('view type'),
        required=False,
        help_text=_('How the data is shown on the map. Select "summary view" '
                    'to enable more filters.'),
    )
    choropleth_boundary_layer = forms.ChoiceField(
        choices=(
            ('City Council Districts', _('city council districts')),
            ('Planning Districts', _('planning districts')),
            ('zipcodes', _('zipcodes')),
        ),
        initial='City Council Districts',
        label=_('boundaries'),
        required=False,
    )

    participant_types = forms.MultipleChoiceField(
        choices=(
            ('organizers', 'organizers'),
        ),
        initial=(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    owner__in = forms.ModelMultipleChoiceField(
        label=_('Owner'),
        queryset=Owner.objects.filter(owner_type='public'),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )
    owner__owner_type__in = forms.MultipleChoiceField(
        label=_('Owner types'),
        choices=(
            ('mixed', 'mixed / multiple owners'),
            ('private', 'private'),
            ('public', 'public'),
        ),
        initial=('mixed', 'private', 'public',),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    has_available_property = forms.NullBooleanField(
        label=_('Is available property'),
        help_text=_("Is on the PRA's list of available property"),
    )
    has_billing_account = forms.NullBooleanField(
        help_text=_('Have we found an OPA billing account for this property?'),
    )
    has_tax_account = forms.NullBooleanField(
        help_text=_('Have we found a (delinquent) tax account for this '
                    'property?'),
    )
    has_parcel = forms.NullBooleanField(
        help_text=_('Did we find a parcel for this property in the Records '
                    'Department\'s <a href="http://opendataphilly.org/opendata/resource/28/property-parcels/" target="_blank">file</a>?'),
    )
    has_water_parcel = forms.NullBooleanField(
        help_text=_("Did we find a parcel for this property in the Water "
                    "Department's records?"),
    )
    has_land_use_area = forms.NullBooleanField(
        help_text=_('Did we find a land use area for this property in the '
                    'Planning Commission\'s <a href="http://opendataphilly.org/opendata/resource/170/land-use/" target="_blank">land use file</a>?'),
    )
    has_licenses = forms.NullBooleanField(
        label=_('Is licensed as vacant'),
    )
    has_violations = forms.NullBooleanField()

    owner__name__icontains = forms.CharField(
        label=_('Owner name'),
        required=False,
    )

    violations_count = forms.IntegerField(
        required=False,
    )

    zoning_district__zoning_type__in = forms.ModelMultipleChoiceField(
        label=_('Zoning type'),
        queryset=ZoningType.objects.all(),
        widget=ChosenSelectMultiple(attrs={'style': 'width: 100px;',}),
    )

    known_use_existence = forms.MultipleChoiceField(
        choices=(
            ('not in use', _('none')),
            ('in use', _('in use')),
        ),
        initial=('not in use', 'in use',),
        label=_('Known use'),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    known_use__name__in = forms.MultipleChoiceField(
        choices=(),
        label=_('Known use category'),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    water_parcel__impervious_area__lt = forms.IntegerField(
        label=_('% impervious'),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(FiltersForm, self).__init__(*args, **kwargs)
        self.fields['known_use__name__in'].choices = ([('None', 'None'),] +
                                                      self._get_uses())
        for layer in Layer.objects.all():
            self._add_boundary_layer_field(layer)

    def _add_boundary_layer_field(self, layer):
        field_name = 'boundary_%s' % layer.name.replace(' ', '_').lower()
        boundaries = Boundary.objects.order_by_label_numeric(layer=layer)
        self.fields[field_name] = forms.MultipleChoiceField(
            choices=[(b.label, b.label) for b in boundaries],
            initial=(),
            label=_(layer.name),
            widget=ChosenSelectMultiple(attrs={'style': 'width: 100px;',}),
        )

    def _get_uses(self):
        uses = []
        for use in Use.objects.filter(visible=True).order_by('name'):
            uses += [(use.name, use.name),]
        return uses

    def admin_filters(self):
        for field in ('participant_types', 'has_available_property',
                      'has_billing_account', 'has_tax_account', 'has_parcel',
                      'has_land_use_area', 'has_water_parcel',
                      'owner__name__icontains',
                      'water_parcel__impervious_area__lt',):
            yield self[field]

    def view_filters(self):
        for field in ('view_type', 'choropleth_boundary_layer',):
            yield self[field]

    def default_filter_names(self):
        return ('available_property__status__in', 'polygon_area__gt',
                'polygon_area__lt', 'polygon_width__gt', 'polygon_width__lt',
                'known_use_certainty__gt', 'known_use_certainty__lt',)

    def default_filters(self):
        for field_name in self.default_filter_names():
            yield self[field_name]

    def other_filters(self):
        for field in ('boundary_zipcodes', 'boundary_city_council_districts',
                      'zoning_district__zoning_type__in'):
            yield self[field]

    def owners_filters(self):
        for field in ('owner__owner_type__in', 'owner__in',):
            yield self[field]

    def private_filters(self):
        for field in ('has_licenses', 'has_violations', 'violations_count',):
            yield self[field]

    def known_use_filters(self):
        for field in ('known_use_existence', 'known_use__name__in',):
            yield self[field]

    #
    # Filters by view type
    #
    def choropleth_filters(self):
        return (
            'available_property__status__in', 'polygon_area__gt',
            'polygon_area__lt', 'polygon_width__gt', 'polygon_width__lt',
            'owner__owner_type__in', 'view_type', 'choropleth_boundary_layer',
            'participant_types', 'owner__name__icontains', 'owner__in',
            'has_available_property', 'has_billing_account', 'has_tax_account',
            'has_parcel', 'has_water_parcel', 'has_land_use_area',
            'has_licenses', 'has_violations', 'violations_count',
            'zoning_district__zoning_type__in', 'known_use__name__in',
            'water_parcel__impervious_area__lt', 'boundary_zipcodes',
            'boundary_city_council_districts',
            'known_use_certainty__gt', 'known_use_certainty__lt',
            'known_use_existence',
        )

    def tiles_filters(self):
        return ('owner__owner_type__in', 'view_type', 'known_use_existence',)
