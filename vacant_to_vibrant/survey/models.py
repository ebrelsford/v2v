from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

from forms_builder.forms.models import (AbstractFieldEntry, AbstractFormEntry,
                                        Form)


class SurveyFormEntry(AbstractFormEntry):
    """A Form entry that can be associated with any model instance."""
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    survey_form = models.ForeignKey(Form, related_name='survey_entries')

    def __unicode__(self):
        try:
            return 'form (%d), %s (%d) at %s' % (
                self.survey_form.pk,
                self.content_type.name,
                self.object_id,
                self.entry_time.isoformat(),
            )
        except Exception:
            return '%d' % self.pk


class SurveyFieldEntry(AbstractFieldEntry):
    entry = models.ForeignKey('SurveyFormEntry', related_name='fields')
