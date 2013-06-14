from django.forms import HiddenInput, ModelForm

from notify.forms import NotifyOnCreationForm

from .notifications import notify_participants_new_obj
from .models import get_organizer_model, get_watcher_model
from .widgets import PrefixLabelTextInput


class ParticipantForm(ModelForm):

    def __init__(self, *args, **kwargs):
        # add initial value for added_by based on the user kwarg
        kwargs['initial'] = kwargs.get('initial', {})
        user = kwargs.get('user', None)
        if not user or user.is_anonymous(): user = None
        kwargs['initial']['added_by'] = user

        super(ParticipantForm, self).__init__(*args, **kwargs)


class NotifyParticipantsOnCreationForm(NotifyOnCreationForm):

    def send_notifications(self, obj, is_creating):
        super(NotifyParticipantsOnCreationForm, self).send_notifications(obj, is_creating)
        if is_creating:
            notify_participants_new_obj(obj)


class OrganizerForm(NotifyParticipantsOnCreationForm):

    class Meta:
        model = get_organizer_model()
        widgets = {
            'added_by': HiddenInput(),
            'content_type': HiddenInput(),
            'facebook_page': PrefixLabelTextInput('facebook.com/'),
            'object_id': HiddenInput(),
        }


class WatcherForm(ParticipantForm):

    class Meta:
        model = get_watcher_model()
        widgets = {
            'added_by': HiddenInput(),
            'content_type': HiddenInput(),
            'object_id': HiddenInput(),
        }
