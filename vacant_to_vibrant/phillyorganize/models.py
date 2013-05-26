from django.db import models
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


class Organizer(ParticipantMixin, BaseOrganizer):
    vision = models.TextField(_('vision'),
        blank=True,
        null=True,
        help_text=_('What is your vision for this lot?'),
    )


class Watcher(ParticipantMixin, BaseWatcher):
    pass