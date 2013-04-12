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
    object_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta(FormForForm.Meta):
        model = SurveyFormEntry

    def __init__(self, *args, **kwargs):
        # Get the model instance that the resulting entry will be tied to
        initial = kwargs.pop('initial', {})
        content_object = initial.pop('content_object', None)

        super(SurveyFormForForm, self).__init__(*args, initial=initial,
                                                **kwargs)

        if content_object:
            self.initial.update({
                'content_type': ContentType.objects.get_for_model(content_object),
                'object_id': content_object.pk,
            })

    def save(self, **kwargs):
        # Delete existing entries for this object, if any
        SurveyFormEntry.objects.filter(
            content_type=self.cleaned_data['content_type'],
            object_id=self.cleaned_data['object_id'],
        ).delete()
        return super(SurveyFormForForm, self).save(**kwargs)
