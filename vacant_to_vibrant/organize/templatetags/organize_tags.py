"""
Template tags for the organize app, loosely based on django.contrib.comments.

"""
from django import template
from django.contrib.contenttypes.models import ContentType

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag, InclusionTag

from organize.models import Organizer

register = template.Library()


class OrganizersMixin(object):

    def get_organizers(self, target):
        return Organizer.objects.filter(
            content_type=ContentType.objects.get_for_model(target),
            object_id=target.pk,
        )


class RenderOrganizerList(OrganizersMixin, InclusionTag):
    name = 'render_organizer_list'
    options = Options(
        'for',
        Argument('target', required=True, resolve=True)
    )
    template = 'organize/organizer_list.html'

    def get_context(self, context, target):
        context.update({
            'organizers': self.get_organizers(target),
        })
        return context

register.tag(RenderOrganizerList)


class GetOrganizerList(OrganizersMixin, AsTag):
    name = 'get_organizer_list'
    options = Options(
        'for',
        Argument('target', required=True, resolve=True),
        'as',
        Argument('varname', required=True, resolve=False),
    )

    def get_value(self, context, target):
        print 'get_value', target
        return self.get_organizers(target)

register.tag(GetOrganizerList)
