"""
Template tags for the files app, loosely based on django.contrib.comments.

"""
from django import template

from livinglots_generictags.tags import (GetGenericRelationList,
                                         RenderGenericRelationList,
                                         GetGenericRelationCount)

from ..models import File

register = template.Library()


class RenderFileList(RenderGenericRelationList):
    model = File

register.tag(RenderFileList)


class GetFileList(GetGenericRelationList):
    model = File

register.tag(GetFileList)


class GetFileCount(GetGenericRelationCount):
    model = File

register.tag(GetFileCount)
