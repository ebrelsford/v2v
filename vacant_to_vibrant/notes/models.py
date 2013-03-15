from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Note(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    author = models.CharField(_('author'), max_length=256, null=True,
                              blank=True)
    subject = models.CharField(_('subject'), max_length=256, null=True,
                               blank=True)
    text = models.TextField(_('text'), null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return self.subject
