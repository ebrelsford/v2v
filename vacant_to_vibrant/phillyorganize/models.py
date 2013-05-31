from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from libapps.organize.models import BaseOrganizer, BaseWatcher


class ParticipantMixin(models.Model):
    receive_text_messages = models.BooleanField(_('receive text messages'),
        default=False,
        help_text=_('Do you want to get text messages from the Garden Justice '
                    'Legal Initiative about this lot?'),
    )

    class Meta:
        abstract = True


class BasePhillyOrganizer(ParticipantMixin, BaseOrganizer):

    class Meta:
        abstract = True


class Organizer(BasePhillyOrganizer):
    pass


class Watcher(ParticipantMixin, BaseWatcher):
    pass


#
# Handle signals.
#


@receiver(post_save, sender=Organizer,
          dispatch_uid='organizer_subscribe_organizer_watcher')
@receiver(post_save, sender=Watcher,
          dispatch_uid='watcher_subscribe_organizer_watcher')
def subscribe_organizer_watcher(sender, created=False, instance=None, **kwargs):
    if created:
        # TODO subscribe Participant to mailing list
        #subscribe(instance, is_participating=True)
        pass
