from django import forms
from django.utils.translation import ugettext_lazy as _

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
    )
    has_billing_account = forms.NullBooleanField()
    has_tax_account = forms.NullBooleanField()
    has_parcel = forms.NullBooleanField()
    has_land_use_area = forms.NullBooleanField()
    has_violations = forms.NullBooleanField()

    violations_count = forms.IntegerField(
        required=False,
    )

    zoning_district__zoning_type__in = forms.ModelMultipleChoiceField(
        queryset=ZoningType.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
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
            widget=forms.CheckboxSelectMultiple(),
        )

    def _get_uses(self):
        uses = []
        for use in Use.objects.all().order_by('name'):
            uses += [(use.name, use.name),]
        return uses
