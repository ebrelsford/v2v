import autocomplete_light

from .models import Owner


autocomplete_light.register(Owner,
    search_fields=['name',],
    # This will actually data-minimum-characters which will set
    # widget.autocomplete.minimumCharacters.
    autocomplete_js_attributes={'placeholder': 'Other model name ?',},
)
