from hashlib import sha1

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class Participant(models.Model):
    """
    A person who is participating in something and who wishes to receive
    updates about the thing.
    """
    name = models.CharField(_('name'), max_length=256)
    phone = models.CharField(_('phone'), max_length=32, null=True, blank=True)
    email = models.EmailField(_('email'))
    email_hash = models.CharField(max_length=40, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, null=True, blank=True)

    target_type = models.ForeignKey(ContentType)
    target_id = models.PositiveIntegerField()
    target = generic.GenericForeignKey('target_type', 'target_id')

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.email:
            self.email_hash = sha1(settings.ORGANIZE_PARTICIPANT_SALT +
                                   self.email).hexdigest()
        super(Participant, self).save(*args, **kwargs)


class Organizer(Participant):
    """
    Someone publicly participating in something.
    """
    # so we can do spatial joins between Organizer and Lot
    objects = models.GeoManager()

    type = models.ForeignKey('OrganizerType')
    url = models.URLField(_('url'), null=True, blank=True)
    notes = models.TextField(_('notes'), null=True, blank=True)
    facebook_page = models.CharField(
        _('facebook page'),
        max_length=256,
        null=True,
        blank=True,
        help_text=('The Facebook page for your organization. Please do not '
                   'enter your personal Facebook page.'),
    )

    def recent_change_label(self):
        return 'new organizer: %s' % self.name

    class Meta:
        permissions = (
            ('email_organizers', 'Can send an email to all organizers'),
        )

    def get_absolute_url(self):
        return "%s#organizer-%d" % (self.target.get_absolute_url(), self.pk)


class Watcher(Participant):
    """
    Someone who is privately participating in something.
    """
    # so we can do spatial joins between Watcher and Lot
    objects = models.GeoManager()

    def recent_change_label(self):
        return 'new watcher'


class OrganizerType(models.Model):
    """
    A type of organizer (eg, individual, non-profit, governmental agency, ...).
    """
    name = models.CharField(max_length=64)
    is_group = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


#
# Handle signals.
#
from activity_stream.signals import action


def _get_verb(sender):
    default = 'added'
    if isinstance(sender, Organizer):
        return 'started organizing'
    if isinstance(sender, Watcher):
        return 'started watching'
    return default


def _get_actor(instance, added_by):
    default = added_by

    # Hold on to Organizer instance as actor
    if isinstance(instance, Organizer):
        return instance

    # Don't keep track of the user who created the Watcher--keep anonymous
    if isinstance(instance, Watcher):
        return None

    return default


@receiver(post_save, sender=Organizer, dispatch_uid='organize.models.add_action')
@receiver(post_save, sender=Watcher, dispatch_uid='organize.models.add_action')
def add_action(sender, created=False, instance=None, **kwargs):
    if not instance or not created:
        return
    action.send(
        _get_actor(instance, instance.added_by),
        verb=_get_verb(instance),
        action_object=instance, # action object, what was created
        # TODO fix...
        #place=instance.target.centroid, # where did it happen?
        target=instance.target, # what did it happen to?
        data={},
    )


@receiver(post_save, sender=Organizer, dispatch_uid='organizer_subscribe_organizer_watcher')
@receiver(post_save, sender=Watcher, dispatch_uid='watcher_subscribe_organizer_watcher')
def subscribe_organizer_watcher(sender, created=False, instance=None, **kwargs):
    if created:
        # TODO subscribe Participant to mailing list
        #subscribe(instance, is_participating=True)
        pass
