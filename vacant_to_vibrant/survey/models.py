from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

from forms_builder.forms.models import AbstractFieldEntry, AbstractFormEntry


class SurveyFormEntry(AbstractFormEntry):
    """A Form entry that can be associated with any model instance."""
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')


class SurveyFieldEntry(AbstractFieldEntry):
    entry = models.ForeignKey('SurveyFormEntry', related_name='fields')
