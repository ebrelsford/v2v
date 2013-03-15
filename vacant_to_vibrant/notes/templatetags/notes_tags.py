"""
Template tags for the notes app, loosely based on django.contrib.comments.

"""
from django import template
from django.contrib.contenttypes.models import ContentType

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag, InclusionTag

from ..models import Note

register = template.Library()


class NotesMixin(object):

    def get_notes(self, target):
        return Note.objects.filter(
            content_type=ContentType.objects.get_for_model(target),
            object_id=target.pk,
        )


class RenderNoteList(NotesMixin, InclusionTag):
    name = 'render_note_list'
    options = Options(
        'for',
        Argument('target', required=True, resolve=True)
    )
    template = 'notes/note_list.html'

    def get_context(self, context, target):
        return {
            'notes': self.get_notes(target),
        }

register.tag(RenderNoteList)


class GetNoteList(NotesMixin, AsTag):
    name = 'get_note_list'
    options = Options(
        'for',
        Argument('target', required=True, resolve=True),
        'as',
        Argument('varname', required=True, resolve=False),
    )

    def get_value(self, context, target):
        return self.get_notes(target)

register.tag(GetNoteList)
