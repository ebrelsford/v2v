"""
Template tags for the photos app, loosely based on django.contrib.comments.

"""
from django import template
from django.contrib.contenttypes.models import ContentType

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag, InclusionTag

from photos.models import Photo

register = template.Library()


class PhotosMixin(object):

    def get_photos(self, target):
        return Photo.objects.filter(
            content_type=ContentType.objects.get_for_model(target),
            object_id=target.pk,
        )


class RenderPhotoList(PhotosMixin, InclusionTag):
    name = 'render_photo_list'
    options = Options(
        'for',
        Argument('target', required=True, resolve=True)
    )
    template = 'photos/photo_list.html'

    def get_context(self, context, target):
        return {
            'photos': self.get_photos(target),
        }

register.tag(RenderPhotoList)


class GetPhotoList(PhotosMixin, AsTag):
    name = 'get_photo_list'
    options = Options(
        'for',
        Argument('target', required=True, resolve=True),
        'as',
        Argument('varname', required=True, resolve=False),
    )

    def get_value(self, context, target):
        return self.get_photos(target)

register.tag(GetPhotoList)
