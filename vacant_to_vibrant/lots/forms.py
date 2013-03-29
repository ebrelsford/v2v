from django import forms


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

    # TODO lot filters! Dynamically add to form?
