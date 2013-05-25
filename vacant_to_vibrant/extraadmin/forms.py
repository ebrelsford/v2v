from django import forms
from django.http import QueryDict


class MailParticipantsForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    filters = forms.CharField(widget=forms.HiddenInput)

    def clean_filters(self):
        return QueryDict(self.cleaned_data['filters'])

    def clean(self):
        cleaned_data = super(MailParticipantsForm, self).clean()
        filters = cleaned_data.get('filters')

        # Ensure participant types are selected
        try:
            participant_types = filters['participant_types']
        except Exception:
            participant_types = None
        if not participant_types:
            raise forms.ValidationError("Pick a participant type or the email "
                                        "won't go to anyone!")

        return cleaned_data
