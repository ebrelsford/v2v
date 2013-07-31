from django.db import models
from django.utils.translation import ugettext_lazy as _

import django_monitor
from livinglots_groundtruth.models import BaseGroundtruthRecord


class GroundtruthRecord(BaseGroundtruthRecord):

    use = models.ForeignKey('lots.Use',
        verbose_name=_('use'),
        limit_choices_to={'visible': False},
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
