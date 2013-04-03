from django import forms
from django.utils.translation import ugettext_lazy as _

from inplace.boundaries.models import Boundary, Layer

from .models import Use


class FiltersForm(forms.Form):
    centroid__within = forms.CharField(widget=forms.HiddenInput)
    limit = forms.CharField(widget=forms.HiddenInput, initial='1000')

    participant_types = forms.MultipleChoiceField(
        choices=(
            ('organizers', 'organizers'),
            ('watchers', 'watchers'),
        ),
        initial=(),
        widget=forms.CheckboxSelectMultiple(attrs={ 'class': 'filter', }),
    )

    owner__name__icontains = forms.CharField(label='owner name')
    owner__owner_type__in = forms.MultipleChoiceField(
        label='owner types',
        choices=(
            ('private', 'private'),
            ('public', 'public'),
            ('unknown', 'unknown'),
        ),
        initial=(),
        widget=forms.CheckboxSelectMultiple(attrs={ 'class': 'filter', }),
    )

    has_available_property = forms.NullBooleanField()
    has_billing_account = forms.NullBooleanField()
    has_tax_account = forms.NullBooleanField()
    has_parcel = forms.NullBooleanField()
    has_land_use_area = forms.NullBooleanField()
    has_violations = forms.NullBooleanField()

    violations_count = forms.IntegerField()

    known_use__name__in = forms.MultipleChoiceField(
        choices=(),
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
