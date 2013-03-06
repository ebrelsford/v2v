from django import template
from django.template.loader import render_to_string
register = template.Library()


@register.tag
def place_map(parser, token):
    """
    Display a map.

    {% place_map <places_url> [<width> <height>] [<zoom>] [using <template_name>] %}
    """
    width, height, zoom, template_name = None, None, None, None
    params = token.split_contents()

    # pop the template name
    if params[-2] == 'using':
        template_name = params[-1]
        params = params[:-2]

    if len(params) < 2:
        raise template.TemplateSyntaxError('place_map tag requires places_url '
                                           'argument')

    places_url = params[1]

    if len(params) == 4:
        width, height = params[2], params[3]
    elif len(params) == 5:
        width, height, zoom = params[2], params[3], params[4]
    elif len(params) == 3 or len(params) > 5:
        raise template.TemplateSyntaxError(
            'place_map tag has the following syntax: '
            '{% place_map <places_url> <width> <height> [zoom] [using <template_name>] %}')
    return PlaceMapNode(places_url, width, height, zoom, template_name)


class PlaceMapNode(template.Node):
    def __init__(self, places_url, width, height, zoom, template_name):
        self.places_url = template.Variable(places_url)
        self.width = width or ''
        self.height = height or ''
        self.zoom = zoom or 16
        self.template_name = template.Variable(template_name or '"places/cloudmade/map.html"')

    def render(self, context):
        try:
            places_url = self.places_url.resolve(context)
            template_name = self.template_name.resolve(context)

            context.update({
                'places_url': places_url,
                'width': self.width,
                'height': self.height,
                'zoom': self.zoom,
                'template_name': template_name
            })
            return render_to_string(template_name, context_instance=context)
        except template.VariableDoesNotExist:
            return ''
