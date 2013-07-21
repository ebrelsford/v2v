from libapps.organize import forms as organize_forms


class OrganizerForm(organize_forms.OrganizerForm):
    class Meta(organize_forms.OrganizerForm.Meta):
        exclude = ('notes',)
