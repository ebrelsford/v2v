from django import forms

from notify.forms import NotifyOnCreationForm
from .models import StewardNotification


class StewardNotificationForm(NotifyOnCreationForm):

    class Meta:
        model = StewardNotification
        fields = (
            # Hidden fields
            'content_type', 'object_id',

            # Organizer fields
            'name', 'phone', 'email', 'type', 'url', 'facebook_page',

            # StewardProject fields
            'use', 'land_tenure_status', 'support_organization',
            'others_get_involved', 'farm_stand', 'waiting_list',
            'include_on_map',
        )
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }
