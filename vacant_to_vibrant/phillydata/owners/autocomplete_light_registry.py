import autocomplete_light

from .models import Owner


autocomplete_light.register(Owner,
    search_fields=['name',],
    autocomplete_js_attributes={'placeholder': 'Owner name',},
)
