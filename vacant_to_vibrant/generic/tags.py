"""
Helpers for creating template tags for models with generic relations.

"""
from django.contrib.contenttypes.models import ContentType

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag, InclusionTag


class GenericRelationMixin(object):

    def get_objects(self, target):
        return self.model.objects.filter(
            content_type=ContentType.objects.get_for_model(target),
            object_id=target.pk,
        )


class RenderGenericRelationList(GenericRelationMixin, InclusionTag):
    options = Options(
        'for',
        Argument('target', required=True, resolve=True)
    )

    # NB: unfortunately required
    template = ''

    def get_context(self, context, target):
        return {
            self.get_model_plural_name(): self.get_objects(target),
        }

    def get_template(self, context, **kwargs):
        return '%s/%s_list.html' % (
            self.model._meta.app_label,
            self.model._meta.object_name.lower(),
        )

    def get_model_plural_name(self):
        return self.model._meta.object_name.lower() + 's'


class GetGenericRelationList(GenericRelationMixin, AsTag):
    options = Options(
        'for',
        Argument('target', required=True, resolve=True),
        'as',
        Argument('varname', required=True, resolve=False),
    )

    def get_value(self, context, target):
        return self.get_objects(target)
