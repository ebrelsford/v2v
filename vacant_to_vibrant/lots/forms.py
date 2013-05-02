from django import forms
from django.utils.translation import ugettext_lazy as _

from chosen.forms import ChosenSelectMultiple
from inplace.boundaries.models import Boundary, Layer

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
    limit = forms.CharField(
        initial='1000',
        required=False,
        widget=forms.HiddenInput,
    )
    parents_only = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput
    )

    participant_types = forms.MultipleChoiceField(
        choices=(
            ('organizers', 'organizers'),
            ('watchers', 'watchers'),
        ),
        initial=(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={ 'class': 'filter', }),
    )

    owner__name__icontains = forms.CharField(
        label=_('Owner name'),
        required=False,
    )
    owner__owner_type__in = forms.MultipleChoiceField(
        label=_('Owner types'),
        choices=(
            ('private', 'private'),
            ('public', 'public'),
            ('unknown', 'unknown'),
        ),
        initial=(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={ 'class': 'filter', }),
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
    has_land_use_area = forms.NullBooleanField(
        help_text=_('Did we find a land use area for this property in the '
                    'Planning Commission\'s <a href="http://opendataphilly.org/opendata/resource/170/land-use/" target="_blank">land use file</a>?'),
    )
    has_violations = forms.NullBooleanField()

    violations_count = forms.IntegerField(
        required=False,
    )

    zoning_district__zoning_type__in = forms.ModelMultipleChoiceField(
        label=_('Zoning type'),
        queryset=ZoningType.objects.all(),
        widget=ChosenSelectMultiple(),
    )

    known_use__name__in = forms.MultipleChoiceField(
        choices=(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={ 'class': 'filter', }),
    )

    # TODO lot filters! Dynamically add to form?

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
            widget=ChosenSelectMultiple(),
        )

    def _get_uses(self):
        uses = []
        for use in Use.objects.all().order_by('name'):
            uses += [(use.name, use.name),]
        return uses

    def admin_filters(self):
        for field in ('participant_types', 'has_available_property',
                      'has_billing_account', 'has_tax_account', 'has_parcel',
                      'has_land_use_area'):
            yield self[field]

    def other_filters(self):
        for field in ('boundary_zipcodes', 'boundary_city_council_districts',
                      'zoning_district__zoning_type__in'):
            yield self[field]

    def owners_filters(self):
        for field in ('owner__name__icontains', 'owner__owner_type__in',):
            yield self[field]

    def private_filters(self):
        for field in ('has_violations', 'violations_count',):
            yield self[field]
