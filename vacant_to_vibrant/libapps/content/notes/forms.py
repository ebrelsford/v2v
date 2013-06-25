from django import forms
from django.utils.translation import ugettext_lazy as _

from ..forms import ContentForm
from .models import Note


class NoteForm(ContentForm):

    added_by_name = forms.CharField(
        label=_('Your name'),
        max_length=256,
        required=True,
        widget=forms.TextInput(),
    )

    class Meta:
        fields = ('added_by_name', 'text', 'content_type', 'object_id',)
        model = Note
