from django.forms import (Form, CharField, Textarea, MultipleChoiceField,
                          HiddenInput, CheckboxSelectMultiple)


class MailParticipantsForm(Form):
    subject = CharField()
    message = CharField(widget=Textarea)

    centroid__within = CharField(required=False, widget=HiddenInput)

    participant_types = MultipleChoiceField(
        choices=(
            ('organizers', 'organizers'),
            ('watchers', 'watchers'),
        ),
        initial=('organizers', 'watchers'),
        widget=CheckboxSelectMultiple(attrs={ 'class': 'filter', }),
    )

    # TODO lot filters! Dynamically add to form?
