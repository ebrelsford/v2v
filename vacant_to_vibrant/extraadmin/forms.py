from django import forms

from lots.forms import FiltersForm


class MailForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)


class MailParticipantsForm(MailForm, FiltersForm):
    pass
