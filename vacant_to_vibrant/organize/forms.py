from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.forms import HiddenInput, IntegerField, ModelForm, ModelChoiceField

from recaptcha_works.fields import RecaptchaField

from notify import notify_organizers_and_watchers, notify_facilitators
from models import Organizer, Watcher
from widgets import PrefixLabelTextInput


class CaptchaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CaptchaForm, self).__init__(*args, **kwargs)

        # if not logged in, add recaptcha. else, do nothing.
        if not user or user.is_anonymous():
            self.fields['recaptcha'] = RecaptchaField(label="Prove you're human")


class ParticipantForm(CaptchaForm):
    target_type = ModelChoiceField(
        label='target type',
        queryset=ContentType.objects.all(),
        widget=HiddenInput()
    )
    target_id = IntegerField(
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

    def save(self, force_insert=False, force_update=False, commit=True):
        is_creating = False
        if not self.instance.id:
            is_creating = True

        organizer = super(self.__class__, self).save()
        if is_creating:
            notify_organizers_and_watchers(organizer)
            notify_facilitators(organizer)
        return organizer


class WatcherForm(ParticipantForm):
    class Meta:
        model = Watcher
        exclude = ('added', 'email_hash')
