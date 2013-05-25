"""
Template tags for the notes app, loosely based on django.contrib.comments.

"""
from django import template

from generic.tags import GetGenericRelationList, RenderGenericRelationList
from ..models import Photo

register = template.Library()


class RenderPhotoList(RenderGenericRelationList):
    model = Photo

register.tag(RenderPhotoList)

class GetPhotoList(GetGenericRelationList):
    model = Photo

register.tag(GetPhotoList)
