"""
Template tags for the organize app, loosely based on django.contrib.comments.

"""
from django import template

from generic.tags import (GetGenericRelationCount, GetGenericRelationList,
                          RenderGenericRelationList)
from ..models import Organizer, Watcher

register = template.Library()


class RenderOrganizerList(RenderGenericRelationList):
    model = Organizer

register.tag(RenderOrganizerList)


class GetOrganizerList(GetGenericRelationList):
    model = Organizer

register.tag(GetOrganizerList)


class GetOrganizerCount(GetGenericRelationCount):
    model = Organizer

register.tag(GetOrganizerCount)


class GetWatcherCount(GetGenericRelationCount):
    model = Watcher

register.tag(GetWatcherCount)
