from django import forms

from .models import GroundtruthRecord


class GroundtruthRecordForm(forms.ModelForm):

    class Meta:
        model = GroundtruthRecord
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
            'use': forms.HiddenInput(),
        }
