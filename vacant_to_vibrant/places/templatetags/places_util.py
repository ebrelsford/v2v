from django import template
from django.conf import settings
register = template.Library()


@register.tag
def places_setting(parser, token):
    """
    Get a places setting.

    {% places_setting <setting_name> %}
    """
    setting_name = None
    params = token.split_contents()

    if len(params) == 2:
        setting_name = params[1]
    else:
        raise template.TemplateSyntaxError(
            'places_setting tag has the following syntax: '
            '{% places_setting <setting_name>')
    return PlacesSettingNode(setting_name)


class PlacesSettingNode(template.Node):
    def __init__(self, setting_name):
        self.setting_name = setting_name

    def render(self, context):
        try:
            return getattr(settings, self.setting_name)
        except template.VariableDoesNotExist:
            return ''
        except AttributeError:
            return ''
