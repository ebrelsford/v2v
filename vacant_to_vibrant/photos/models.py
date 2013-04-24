from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ImageSpecField
from imagekit.processors.resize import SmartResize


class Photo(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    original_image = models.ImageField(_('original image'), upload_to='photos')
    formatted_image = ImageSpecField(
        format='JPEG',
        options={'quality': 90},
        source='original_image',
    )
    thumbnail = ImageSpecField(
        [SmartResize(200, 200)],
        format='JPEG',
        options={'quality': 90},
        source='original_image',
    )

    name = models.CharField(_('name'), max_length=256, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, null=True, blank=True)
    added_by_name = models.CharField(_('added by name'), max_length=256,
                                     null=True, blank=True)

    def __unicode__(self):
        return self.name
