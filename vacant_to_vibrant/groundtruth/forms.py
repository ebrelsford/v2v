from django import forms

from livinglots_groundtruth.forms import GroundtruthRecordFormMixin

from .models import GroundtruthRecord


class GroundtruthRecordForm(GroundtruthRecordFormMixin, forms.ModelForm):

    class Meta:
        model = GroundtruthRecord
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
            'use': forms.HiddenInput(),
        }
