"""
Template tags for the notes app, loosely based on django.contrib.comments.

"""
from django import template

from generic.tags import GetGenericRelationList, RenderGenericRelationList
from ..models import Note

register = template.Library()


class RenderNoteList(RenderGenericRelationList):
    model = Note

register.tag(RenderNoteList)

class GetNoteList(GetGenericRelationList):
    model = Note

register.tag(GetNoteList)
