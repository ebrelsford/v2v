from django.db.models import Q
from django.forms import (Form, CharField, Textarea, MultipleChoiceField,
                          HiddenInput, CheckboxSelectMultiple)

from lots.models import Lot


class MailParticipantsForm(Form):
    subject = CharField()
    message = CharField(widget=Textarea)

    bbox = CharField(required=False, widget=HiddenInput)

    participant_types = MultipleChoiceField(
        choices=(
            ('organizers', 'organizers'),
            ('watchers', 'watchers'),
        ),
        initial=('organizers', 'watchers'),
        widget=CheckboxSelectMultiple(attrs={ 'class': 'filter', }),
    )

    # TODO lot filters! Dynamically add to form?

    def __init__(self, *args, **kwargs):
        super(MailParticipantsForm, self).__init__(*args, **kwargs)

        lots = Lot.objects.filter(
            # TODO replace functionality (only getting lots with participants)
            #~Q(organizer=None) | ~Q(watcher=None),
        )
