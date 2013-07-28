"""
Template tags for the organize app, loosely based on django.contrib.comments.

"""
from django import template

from livinglots_generictags.tags import (GetGenericRelationList,
                                         RenderGenericRelationList,
                                         GetGenericRelationCount)

from ..models import get_organizer_model, get_watcher_model

register = template.Library()


class RenderOrganizerList(RenderGenericRelationList):
    model = get_organizer_model()

register.tag(RenderOrganizerList)


class GetOrganizerList(GetGenericRelationList):
    model = get_organizer_model()

register.tag(GetOrganizerList)


class GetOrganizerCount(GetGenericRelationCount):
    model = get_organizer_model()

register.tag(GetOrganizerCount)


class GetWatcherCount(GetGenericRelationCount):
    model = get_watcher_model()

register.tag(GetWatcherCount)
