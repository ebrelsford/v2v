from autocomplete_light import AutocompleteModelBase, register

from .models import Owner


class OwnerAutocomplete(AutocompleteModelBase):
    autocomplete_js_attributes = {'placeholder': 'Owner name',}
    search_fields = ('name',)


register(Owner, OwnerAutocomplete)
