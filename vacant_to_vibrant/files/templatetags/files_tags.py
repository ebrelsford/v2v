"""
Template tags for the files app, loosely based on django.contrib.comments.

"""
from django import template

from generic.tags import GetGenericRelationList, RenderGenericRelationList
from ..models import File

register = template.Library()


class RenderFileList(RenderGenericRelationList):
    model = File

register.tag(RenderFileList)

class GetFileList(GetGenericRelationList):
    model = File

register.tag(GetFileList)
