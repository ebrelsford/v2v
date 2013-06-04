from django import forms

from notify.forms import NotifyOnCreationForm
from .models import GroundtruthRecord


class GroundtruthRecordForm(NotifyOnCreationForm):

    class Meta:
        model = GroundtruthRecord
        exclude = ('added',)
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }
