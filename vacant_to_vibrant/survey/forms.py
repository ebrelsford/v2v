from django import forms
from django.contrib.contenttypes.models import ContentType

from forms_builder.forms.forms import FormForForm

from .models import SurveyFieldEntry, SurveyFormEntry


class SurveyFormForForm(FormForForm):
    field_entry_model = SurveyFieldEntry

    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.all(),
        widget=forms.HiddenInput,
    )

    class Meta(FormForForm.Meta):
        model = SurveyFormEntry
        widgets = {
            'object_id': forms.HiddenInput,
            'survey_form': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        # Get the model instance that the resulting entry will be tied to
        initial = kwargs.pop('initial', {})
        content_object = initial.pop('content_object', None)
        survey_form = initial.pop('survey_form', None)

        super(SurveyFormForForm, self).__init__(*args, initial=initial, **kwargs)

        if content_object:
            self.initial.update({
                'content_type': ContentType.objects.get_for_model(content_object),
                'object_id': content_object.pk,
                'survey_form': survey_form,
            })
