from django import template

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag

from ..models import Pathway

register = template.Library()


class GetPathways(AsTag):
    options = Options(
        'for',
        Argument('target', required=True, resolve=True),
        'as',
        Argument('varname', required=True, resolve=False),
    )

    def get_value(self, context, target):
        return Pathway.objects.get_for_lot(target)

register.tag(GetPathways)
