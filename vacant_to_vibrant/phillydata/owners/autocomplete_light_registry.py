from autocomplete_light import AutocompleteModelBase, register

from .models import Owner


class OwnerAutocomplete(AutocompleteModelBase):
    autocomplete_js_attributes = {'placeholder': 'Owner name',}
    search_fields = ('name',)

    def choices_for_request(self):
        choices = super(OwnerAutocomplete, self).choices_for_request()

        if not self.request.user.is_staff:
            choices = choices.none()

        return choices

register(Owner, OwnerAutocomplete)
