from django import template
from django.contrib.contenttypes.models import ContentType

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import InclusionTag

from ..models import SurveyFormEntry

from forms_builder.forms.models import Form

register = template.Library()


class RenderSurveyEntry(InclusionTag):
    options = Options(
        Argument('form', required=True, resolve=True),
        'for',
        Argument('target', required=True, resolve=True)
    )
    template = 'survey/entry.html'

    def get_entry(self, form, target):
        return SurveyFormEntry.objects.filter(
            content_type=ContentType.objects.get_for_model(target),
            object_id=target.pk,
            survey_form=form,
        ).order_by('-entry_time')[0]

    def get_form_entry_values(self, survey_form, form_entry):
        current_values = []
        for field_entry in form_entry.fields.all():
            field = survey_form.fields.get(pk=field_entry.field_id)
            value = field_entry.value
            current_values.append((field, value))
        return current_values

    def get_context(self, context, form=None, target=None):
        try:
            survey_form = Form.objects.get(pk=form)
            form_entry = self.get_entry(survey_form, target)
            context.update({
                'current_values': self.get_form_entry_values(survey_form, form_entry),
            })
        except Exception:
            pass
        return context

    def get_template(self, context, **kwargs):
        return 'survey/entry_%d.html' % kwargs['form']

register.tag(RenderSurveyEntry)
