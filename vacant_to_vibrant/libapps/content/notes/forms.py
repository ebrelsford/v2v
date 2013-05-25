from ..forms import ContentForm
from .models import Note


class NoteForm(ContentForm):

    class Meta:
        fields = ('added_by_name', 'subject', 'text', 'content_type',
                  'object_id',)
        model = Note
