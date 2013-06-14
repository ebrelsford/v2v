from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe

class PrefixLabelTextInput(TextInput):
    def __init__(self, prefix):
        super(PrefixLabelTextInput, self).__init__()
        self.prefix = prefix

    def render(self, name, value, attrs=None):
        attributes = { 'class': 'prefixed' }
        if attrs:
            attributes = dict(attributes.items() + attrs.items())
        rendered_field = super(PrefixLabelTextInput, self).render(name, value, attributes)
        return mark_safe("""
            <div class="input-prepend">
                <span class="add-on prefix">%s</span> %s
            </div>
        """ % (self.prefix, rendered_field))


