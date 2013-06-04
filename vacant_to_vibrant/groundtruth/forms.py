from django import forms

from notify.forms import NotifyOnCreationForm
from .models import GroundtruthRecord


class GroundtruthRecordForm(NotifyOnCreationForm):

    def get_should_notify_facilitators(self, obj):
        # Don't bother notifying facilitators of the object was auto-moderated
        # and approved
        return self.should_notify_facilitators and not obj.is_approved

    class Meta:
        model = GroundtruthRecord
        exclude = ('added',)
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }
