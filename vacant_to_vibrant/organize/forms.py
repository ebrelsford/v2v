from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.forms import HiddenInput, IntegerField, ModelChoiceField

from notify import notify_participants_new_obj, notify_facilitators
from models import Organizer, Watcher
from vacant_to_vibrant.forms import CaptchaForm
from .widgets import PrefixLabelTextInput


class ParticipantForm(CaptchaForm):
    content_type = ModelChoiceField(
        label='target type',
        queryset=ContentType.objects.all(),
        widget=HiddenInput()
    )
    object_id = IntegerField(
        label='target id',
        widget=HiddenInput()
    )

    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        required=False,
        widget=HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        # add initial value for added_by based on the user kwarg
        kwargs['initial'] = kwargs.get('initial', {})
        user = kwargs.get('user', None)
        if not user or user.is_anonymous(): user = None
        kwargs['initial']['added_by'] = user

        super(ParticipantForm, self).__init__(*args, **kwargs)


class OrganizerForm(ParticipantForm):
    class Meta:
        exclude = ('added', 'email_hash')
        model = Organizer
        widgets = {
            'facebook_page': PrefixLabelTextInput('facebook.com/'),
        }

    def save(self, **kwargs):
        is_creating = False
        if not self.instance.id:
            is_creating = True

        organizer = super(self.__class__, self).save(**kwargs)
        if is_creating:
            notify_participants_new_obj(organizer)
            notify_facilitators(organizer)
        return organizer


class WatcherForm(ParticipantForm):
    class Meta:
        model = Watcher
        exclude = ('added', 'email_hash')
