"""
Template tags for the organize app, loosely based on django.contrib.comments.

"""
from django import template

from generic.tags import GetGenericRelationList, RenderGenericRelationList
from ..models import Organizer

register = template.Library()


class RenderOrganizerList(RenderGenericRelationList):
    model = Organizer

register.tag(RenderOrganizerList)


class GetOrganizerList(GetGenericRelationList):
    model = Organizer

register.tag(GetOrganizerList)
