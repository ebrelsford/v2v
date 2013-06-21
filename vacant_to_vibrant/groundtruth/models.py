from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

import django_monitor


class GroundtruthRecord(models.Model):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    use = models.ForeignKey('lots.Use',
        verbose_name=_('use'),
        limit_choices_to={'visible': False},
    )
    actual_use = models.TextField(_('actual use'),
        help_text=_('How is the lot actually being used?'),
    )
    contact_email = models.EmailField(_('contact email'),
        blank=True,
        null=True,
        help_text=_('Who can we email for more information?'),
    )
    contact_phone = models.CharField(_('contact phone'),
        blank=True,
        null=True,
        max_length = 20,
        help_text=_('Who can we call for more information?'),
    )
    added = models.DateTimeField(_('date added'),
        auto_now_add=True,
        editable=False,
        help_text=('When this lot was added'),
    )


django_monitor.nq(GroundtruthRecord)

# Disconnect monitor's post-save handler
from django.db.models.signals import post_save

from django_monitor.util import save_handler

post_save.disconnect(save_handler, sender=GroundtruthRecord)


#
# Signals
#
from django.dispatch import receiver

from django_monitor import post_moderation


@receiver(post_moderation, sender=GroundtruthRecord,
          dispatch_uid='groundtruth_groundtruthrecord')
def update_use(sender, instance, **kwargs):
    """
    Once a GroundtruthRecord is moderated and approved, make it official by
    updating the use on the referred-to Lot.
    """
    if not instance.is_approved or not instance.content_object:
        return

    lot = instance.content_object

    lot.known_use = instance.use
    lot.known_use_certainty = 10
    lot.known_use_locked = True
    lot.save()
